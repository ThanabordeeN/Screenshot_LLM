import os
import base64
import markdown
from PyQt6.QtWidgets import QMainWindow, QMessageBox , QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
from .interface import Ui_MainWindow  # Import the generated UI class
from .local_generate import Worker_Local
from .litellm_generate import Worker_litellm
import dotenv

USER_ROLE = "user"
AI_ROLE = "assistant"

class ScreenshotAnalyzer(QMainWindow, Ui_MainWindow):
    def __init__(self, image_path = None):
        super().__init__()
        self.setupUi(self)  # Call setupUi on the instance
        
        self.image_path = image_path
        self.memory = []
        self.setup_ui()
        self.load_config()
        self.model_id_input.setText(self.LLM_MODEL_ID)
        self.api_key_input.setText(self.LLM_API_MODEL)

        if self.OLLAMA == "1":
            self.ollama_checkbox.setChecked(True)
        else :
            self.ollama_checkbox.setChecked(False)     
        
        if self.DARK_MODE == "1":
            self.dark_mode_checkbox.setChecked(True)
        else:
            self.dark_mode_checkbox.setChecked(False)
        
        
        self.setup_loading_animation()

    def load_config(self):
            dotenv.load_dotenv(override=True)
            self.LLM_API_MODEL = os.getenv("LLM_API_KEY")
            self.LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
            self.OLLAMA = os.getenv("OLLAMA")        
            self.DARK_MODE = os.getenv("DARK_MODE")

    def setup_ui(self):
        self.display_image()
        self.conversation.setReadOnly(True)
        self.send_button.clicked.connect(self.send_text)
        self.reset_memory.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_config)
        self.reset_config.clicked.connect(self.reset_configurations)
        self.entry.returnPressed.connect(self.send_text)
        self.entry.setFocus()
        self.loading_label.setText("")
    
    def save_config(self):
        LLM_API_MODEL = self.api_key_input.text()
        LLM_MODEL_ID = self.model_id_input.text()
        with open(".env", "w") as env_file:
            env_file.write(f"LLM_API_KEY={LLM_API_MODEL}\n")
            if LLM_MODEL_ID:
                env_file.write(f"LLM_MODEL_ID={LLM_MODEL_ID}\n")
            else:
                env_file.write(f"LLM_MODEL_ID=\n")
            
            if self.ollama_checkbox.isChecked():
                env_file.write(f"OLLAMA=1\n")
            else:
                env_file.write(f"OLLAMA=0\n")
            if self.dark_mode_checkbox.isChecked():
                env_file.write("DARK_MODE=1")
            else :
                env_file.write("DARK_MODE=0")
        self.load_config()
        self.model_id_input.setText(self.LLM_MODEL_ID)
        self.api_key_input.setText(self.LLM_API_MODEL)

        self.show_message("Configuration saved successfully!")

        
    def reset_configurations(self):
        self.LLM_API_MODEL = None
        self.LLM_MODEL_ID = None
        self.OLLAMA = "1"
        self.ollama_checkbox.setChecked(True)
        self.load_config()
        with open(".env", "w") as env_file:
            env_file.write("LLM_API_KEY=\n")
            env_file.write("LLM_MODEL_ID=\n")
            env_file.write("OLLAMA=1\n")
            env_file.write("DARK_MODE=0\n")
        self.show_message("Configuration reset successfully!")
        self.api_key_input.clear()
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
        self.w = int(screen_geometry.width() * 0.20)  # 30% of screen width
        self.h = int(screen_geometry.height() * 0.20)  # 30% of screen height
        pixmap = pixmap.scaled(self.w, self.h, Qt.AspectRatioMode.KeepAspectRatio)
        self.resize(self.w, self.h)
        self.conversation.setMinimumSize(QSize(400, int(self.h/1.2)))
        self.image_label.setMinimumSize(self.w, self.h)
        self.image_label.setPixmap(pixmap)

    def send_text(self):        
        text = self.entry.text().strip()
        if not text:
            return
        self.entry.clear()
        self.update_conversation(text, USER_ROLE)
        self.loading_timer.start()
        self.repaint()
        if len(self.memory) == 0:
            if self.ollama_checkbox.isChecked():
                try:
                    self.memory.append({'role':USER_ROLE, 'content':text , 'images': [self.image_path]})
                except Exception as e:
                    self.show_error_message("No image found")
                    self.loading_label.setText("")
                    return
            else:
                try:                 
                    self.memory.append({
                        'role': USER_ROLE,
                        'content': [
                            {'type': 'text', 'text': text},
                            {'type': 'image_url', 'image_url': 'data:image/png;base64,' + self.image_to_base64()}
                        ]
                    })
                except Exception as e:
                    self.show_error_message("No image found")
                    self.loading_label.setText("")
                    return
        else:
            self.memory.append({'role': USER_ROLE, 'content': text})
        print("Getting response")
        self.load_config()
        if self.OLLAMA == "1":
            print("Using Ollama")
            generator = Worker_Local(self.memory, self.LLM_API_MODEL, self.LLM_MODEL_ID)
            generator.finished.connect(self.finished)
            generator.error.connect(self.show_error_message)
            generator.start()
            self.worker_reference = generator  
        else:
            print("Using Litellm")
            response = Worker_litellm(self.memory, self.LLM_API_MODEL, self.LLM_MODEL_ID)
            response.finished.connect(self.finished)
            response.error.connect(self.show_error_message)
            response.start()
            self.worker_response = response


    def finished(self, response):
        self.loading_timer.stop()
        self.memory.append({'role': AI_ROLE, 'content': response})
        self.loading_label.setText("")
        self.update_conversation(response, AI_ROLE)

    def show_message(self, message):
        message_box = QMessageBox()
        message_box.setWindowTitle("Message")
        message_box.setIcon(QMessageBox.Icon.NoIcon)
        message_box.setWindowModality(Qt.WindowModality.ApplicationModal)
        message_box.setText(message)
        message_box.exec()
    
    def show_error_message(self, error):
        self.loading_timer.stop()
        error_message = QMessageBox()
        red_color = "<font color='red'> {}</font>".format(error)
        error_message.setIcon(QMessageBox.Icon.Critical)
        error_message.setWindowTitle("Error")
        error_message.setWindowModality(Qt.WindowModality.ApplicationModal)
        error_message.setText("Error occurred. Please try again. Error: " + red_color)
        error_message.exec()

    def update_conversation(self, text, role):
        markdown_text = markdown.markdown(text) if role == AI_ROLE else text
        user_color = 'white' if self.dark_mode else 'green'
        ai_color = 'white' if self.dark_mode else 'blue'

        if role == USER_ROLE:
            self.conversation.append(f"😊 : <font color='{user_color}'>{text}</font>")
        else:
            self.conversation.append(f"🤖 : <font color='{ai_color}'>{markdown_text}</font>")

        self.conversation.ensureCursorVisible()

    def image_to_base64(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def setup_loading_animation(self):
        self.loading_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_animation)
        self.loading_timer.setInterval(100)  # Update every 100ms

    def update_loading_animation(self):
        self.loading_label.setText(f"Loading {self.loading_frames[self.current_frame]}")
        self.current_frame = (self.current_frame + 1) % len(self.loading_frames)
