import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtCore
from litellm import completion
import dotenv
import base64
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from interface import Ui_MainWindow  # Import the generated UI class
import markdown
from PyQt5.QtWidgets import QMessageBox

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
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.w = int(screen_width * 0.3)  # 30% of screen width
        self.h = int(screen_height * 0.3)  # 30% of screen height
        pixmap = pixmap.scaled(self.w, self.h, Qt.KeepAspectRatio)
        self.MainWindow.resize(self.w, self.h)
        self.conversation.setMinimumSize(QtCore.QSize(450, int(self.h/1.5)))
        self.image_label.setMinimumSize(self.w, self.h)
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
        self.update_conversation(text, "user")
        self.loading_label.setText("Loading 🔃")
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
       
        try:
            response = self.generate_answer()
            self.memory.append({'role': 'assistant', 'content': response})

            self.loading_label.setText("")
            self.update_conversation(response, "ai")
        except Exception as e:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("Error occurred. Please try again. Error: " + str(e))
            error_message.exec_()
            if os.path.exists(".env"):
                os.remove(".env")
            sys.exit(1)


    def update_conversation(self, text, tag):
        if tag == "ai":
            markdown_text = markdown.markdown(text)
            self.conversation.append(f"<b>AI</b> : <font color='blue'>{markdown_text}</font>")
        else:
            self.conversation.append(f"<b>USER</b> : <font color='green'>{text}</font>")
            
        self.conversation.ensureCursorVisible()

    def image_to_base64(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def generate_answer(self):
        response = completion(
            model=LLM_MODEL_ID,
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

    def __init__(self):
        super().__init__()
        try:
            self.directory = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
            self.current_files = set(os.listdir(self.directory))
        except:
            self.directory = os.path.join(os.path.expanduser("~"),"OneDrive","Pictures", "Screenshots")
            self.current_files = set(os.listdir(self.directory))
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
class ConfigDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Configuration")
            self.layout = QVBoxLayout()

            self.api_key_label = QLabel("LLM API Key:")
            self.api_key_input = QLineEdit()
            self.layout.addWidget(self.api_key_label)
            self.layout.addWidget(QLabel("Get your API key from Provider's website"))
            self.layout.addWidget(self.api_key_input)
            

            self.base_url_label = QLabel("Base URL (optional):")
            self.base_url_input = QLineEdit()
            self.base_url_input.setPlaceholderText("Default is Google AI Studio if left blank")
            self.layout.addWidget(self.base_url_label)
            self.layout.addWidget(QLabel("Get your Base URL from Provider's website"))
            self.layout.addWidget(self.base_url_input)

            self.model_id_label = QLabel("Model ID (optional):")
            self.model_id_input = QLineEdit()
            self.model_id_input.setPlaceholderText("Default is gemini/gemini-1.5-flash-002 if left blank")
            self.layout.addWidget(self.model_id_label)
            self.layout.addWidget(QLabel("Get your Model ID from Provider's website"))
            self.layout.addWidget(self.model_id_input)
                        

            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(self.save_config)
            self.layout.addWidget(self.save_button)

            self.setLayout(self.layout)

        def save_config(self):
            api_key = self.api_key_input.text().strip()
            base_url = self.base_url_input.text().strip()
            model_id = self.model_id_input.text().strip()

            if api_key and base_url=="" and model_id=="":
                with open(".env", "w") as env_file:
                    env_file.write(f"LLM_API_KEY={api_key}\n")
                self.accept()
            elif api_key and base_url and model_id:
                with open(".env", "w") as env_file:
                    env_file.write(f"LLM_API_KEY={api_key}\n")
                    env_file.write(f"BASE_URL={base_url}\n")
                    env_file.write(f"LLM_MODEL_ID={model_id}\n")
                self.accept()
            
            elif api_key and model_id:
                with open(".env", "w") as env_file:
                    env_file.write(f"LLM_API_KEY={api_key}\n")
                    env_file.write(f"LLM_MODEL_ID={model_id}\n")
                self.accept()
            else:
                self.reject()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dotenv.load_dotenv()
    LLM_API_MODEL = os.getenv("LLM_API_KEY")
    AI_BASE_URL = os.getenv("BASE_URL")
    LLM_MODEL_ID = os.getenv("LLM_MODEL_ID","gemini/gemini-1.5-flash-002")

    if not LLM_API_MODEL:
        config_dialog = ConfigDialog()
        if config_dialog.exec_() == QDialog.Accepted:
            dotenv.load_dotenv()
            LLM_API_MODEL = os.getenv("LLM_API_KEY")
            LLM_MODEL_ID = os.getenv("LLM_MODEL_ID","gemini/gemini-1.5-flash-002")
            AI_BASE_URL = os.getenv("BASE_URL")

    print("READY")
    watcher = ScreenshotWatcher()

    def on_screenshot_detected(image_path):
        window = ScreenshotAnalyzer(image_path)
        window.show()
    
    watcher.screenshot_detected.connect(on_screenshot_detected)
    watcher.start()

    sys.exit(app.exec_())