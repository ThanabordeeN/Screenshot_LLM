import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from litellm import completion
import dotenv
import base64
import markdown
from interface import Ui_MainWindow  # Import the generated UI class
from screenshot_watcher import ScreenshotWatcher

USER_ROLE = "user"
AI_ROLE = "assistant"

class ScreenshotAnalyzer(QMainWindow, Ui_MainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setupUi(self)  # Call setupUi on the instance
        self.image_path = image_path
        self.memory = []
        self.setup_ui()
        dotenv.load_dotenv()
        self.LLM_API_MODEL = os.getenv("LLM_API_KEY")
        self.AI_BASE_URL = os.getenv("BASE_URL")
        self.LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")


    def setup_ui(self):
        self.display_image()
        self.conversation.setReadOnly(True)
        self.conversation.append("Ask me anything about this screenshot!\n")
        self.send_button.clicked.connect(self.send_text)
        self.reset_memory.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_config)
        self.reset_config.clicked.connect(self.reset_configurations)
        self.entry.returnPressed.connect(self.send_text)
        self.entry.setFocus()
        self.loading_label.setText("")
    
    def save_config(self):
        LLM_API_MODEL = self.api_key_input.text()
        AI_BASE_URL = self.base_url_input.text()
        LLM_MODEL_ID = self.model_id_input.text()
        if LLM_API_MODEL: 
            with open(".env", "w") as env_file:
                env_file.write(f"LLM_API_KEY={LLM_API_MODEL}\n")
                if AI_BASE_URL:
                    env_file.write(f"BASE_URL={AI_BASE_URL}\n")
                if LLM_MODEL_ID:
                    env_file.write(f"LLM_MODEL_ID={LLM_MODEL_ID}\n")
            self.show_message("Configuration saved successfully!")
            dotenv.load_dotenv(override=True)
            self.LLM_API_MODEL = os.getenv("LLM_API_KEY")
            self.AI_BASE_URL = os.getenv("BASE_URL")
            self.LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
        else:
            self.show_message("Please enter an API key to save configuration.")
        
    def reset_configurations(self):
        self.LLM_API_MODEL = None
        self.AI_BASE_URL = None
        self.LLM_MODEL_ID = None
        with open(".env", "w") as env_file:
            env_file.write("")
        self.show_message("Configuration reset successfully!")
        self.api_key_input.clear()
        self.base_url_input.clear()
        self.model_id_input.clear()
            
        
    def reset(self):
        self.memory = []
        self.conversation.clear()
        self.conversation.append("Ask me anything about this screenshot!\n")
        self.entry.setFocus()

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.w = int(screen_geometry.width() * 0.25)  # 30% of screen width
        self.h = int(screen_geometry.height() * 0.25)  # 30% of screen height
        pixmap = pixmap.scaled(self.w, self.h, Qt.KeepAspectRatio)
        self.MainWindow.resize(self.w, self.h)
        self.conversation.setMinimumSize(QtCore.QSize(450, int(self.h/1.3)))
        self.image_label.setMinimumSize(self.w, self.h)
        self.image_label.setPixmap(pixmap)

    def send_text(self):
        text = self.entry.text().strip()
        if not text:
            return

        self.entry.clear()
        self.update_conversation(text, USER_ROLE)
        self.loading_label.setText("Loading 🔃")
        self.repaint()
        if len(self.memory) == 0:
            self.memory.append({
                'role': USER_ROLE,
                'content': [
                    {'type': 'text', 'text': text},
                    {'type': 'image_url', 'image_url': 'data:image/png;base64,' + self.image_to_base64()}
                ]
            })
        else:
            self.memory.append({'role': USER_ROLE, 'content': text})
        try:
            response = self.generate_answer()
            self.memory.append({'role': AI_ROLE, 'content': response})
            self.loading_label.setText("")
            self.update_conversation(response, AI_ROLE)
        except Exception as e:
            self.show_error_message(str(e))

    def show_message(self, message):
        message_box = QMessageBox()
        message_box.setWindowTitle("Message")
        message_box.setText(message)
        message_box.exec_()
    
    def show_error_message(self, error):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle("Error")
        error_message.setText("Error occurred. Please try again. Error: " + error)
        error_message.exec_()


    def update_conversation(self, text, role):
        markdown_text = markdown.markdown(text) if role == AI_ROLE else text
        self.conversation.append(f"<b>{role.upper()}</b> : <font color='{'blue' if role == AI_ROLE else 'green'}'>{markdown_text}</font>")
        self.conversation.ensureCursorVisible()

    def image_to_base64(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def generate_answer(self):
        try:
            response = completion(
                model="gemini/gemini-1.5-flash-002" if self.LLM_MODEL_ID is None else self.LLM_MODEL_ID,
                base_url=None if self.AI_BASE_URL is None else self.AI_BASE_URL,
                messages=self.memory,
                api_key=None if self.LLM_API_MODEL is None else self.LLM_API_MODEL
            )
            return response.choices[0].message.content
        except Exception as e:
            self.show_error_message(str(e))
            return 
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    watcher = ScreenshotWatcher()

    def on_screenshot_detected(image_path):
        window = ScreenshotAnalyzer(image_path)
        window.show()
    
    watcher.screenshot_detected.connect(on_screenshot_detected)
    watcher.start()

    sys.exit(app.exec_())
