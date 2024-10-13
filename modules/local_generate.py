from PyQt6.QtCore import QThread, pyqtSignal
from ollama import chat

class Worker_Local(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, memory, LLM_API_MODEL, LLM_MODEL_ID):
        super().__init__()
        self.memory = memory
        self.LLM_API_MODEL = LLM_API_MODEL
        self.LLM_MODEL_ID = LLM_MODEL_ID

    def run(self):
        try:
            response = chat(model='minicpm-v:latest' if self.LLM_MODEL_ID == "" else self.LLM_MODEL_ID, 
                            messages=self.memory)
            self.finished.emit(response['message']['content'])
        except Exception as e:
            self.error.emit(str(e))
