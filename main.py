import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtCore
from litellm import completion
import dotenv
import base64
from interface import Ui_MainWindow  # Import the generated UI class

dotenv.load_dotenv()
LLM_API_MODEL = os.getenv("LLM_API_KEY")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID","gemini/gemini-1.5-flash-002")
AI_BASE_URL = os.getenv("BASE_URL")
SCREENSHOTS_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")

class ScreenshotAnalyzer(QMainWindow, Ui_MainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setupUi(self)  # Call setupUi on the instance
        self.image_path = image_path
        self.memory = []
        self.setup_ui()

    def setup_ui(self):
        self.display_image()
        self.setup_conversation_area()
        self.setup_input_area()
        self.setup_loading_label()
        self.bind_events()

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        
        self.w = pixmap.width()
        self.h = pixmap.height()
        self.MainWindow.resize(self.w, self.h)
        self.conversation.setMinimumSize(QtCore.QSize(self.w, int(self.h/2)))
        pixmap = pixmap.scaled(self.w, self.h, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def setup_conversation_area(self):
        self.conversation.setReadOnly(True)
        self.conversation.append("Ask me anything about this screenshot!\n")

    def setup_input_area(self):
        self.send_button.clicked.connect(self.send_text)

    def setup_loading_label(self):
        self.loading_label.setText("")

    def bind_events(self):
        self.entry.returnPressed.connect(self.send_text)
        self.entry.setFocus()

    def send_text(self):
        text = self.entry.text().strip()
        if not text:
            return

        self.entry.clear()
        self.update_conversation("You: " + text, "user")

        self.loading_label.setText("Loading...")
        self.repaint()

        if not self.memory:
            self.memory.append({
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': text},
                    {'type': 'image_url', 'image_url': f'data:image/png;base64,{self.image_to_base64()}'}
                ]
            })
        else:
            self.memory.append({'role': 'user', 'content': text})

        response = self.generate_answer()
        self.memory.append({'role': 'assistant', 'content': response})

        self.loading_label.setText("")
        self.update_conversation("AI: " + response, "ai")

    def update_conversation(self, text, tag):
        self.conversation.append(text)
        self.conversation.ensureCursorVisible()

    def image_to_base64(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def generate_answer(self):
        response = completion(
            model="gemini/gemini-1.5-flash-002",
            base_url=AI_BASE_URL,
            messages=self.memory,
            api_key=LLM_API_MODEL
        )
        return response.choices[0].message.content

    def closeEvent(self, event):
        # Override the close event to hide the window instead of closing it
        event.ignore()
        self.hide()

    def keyPressEvent(self, event):
        # Handle the "Esc" key press to close the window
        if event.key() == Qt.Key_Escape:
            self.close()

class ScreenshotWatcher(QThread):
    screenshot_detected = pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.current_files = set(os.listdir(directory))

    def run(self):
        while True:
            new_files = set(os.listdir(self.directory))
            if new_files != self.current_files:
                added_files = new_files - self.current_files
                if added_files:
                    recent_file = max(
                        added_files,
                        key=lambda f: os.path.getctime(os.path.join(self.directory, f)),
                    )
                    self.screenshot_detected.emit(os.path.join(self.directory, recent_file))
                self.current_files = new_files
            self.msleep(1000)  # Check every second

if __name__ == "__main__":
    app = QApplication(sys.argv)
    watcher = ScreenshotWatcher(SCREENSHOTS_DIR)

    def on_screenshot_detected(image_path):
        window = ScreenshotAnalyzer(image_path)
        window.show()

    watcher.screenshot_detected.connect(on_screenshot_detected)
    watcher.start()

    sys.exit(app.exec_())