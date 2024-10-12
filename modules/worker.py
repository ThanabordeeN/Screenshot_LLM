from PyQt5.QtCore import QThread, pyqtSignal
from litellm import completion
from ollama import chat

class Worker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, memory, ollama_checkbox, LLM_API_MODEL, AI_BASE_URL, LLM_MODEL_ID):
        super().__init__()
        self.memory = memory
        self.ollama_checkbox = ollama_checkbox
        self.LLM_API_MODEL = LLM_API_MODEL
        self.AI_BASE_URL = AI_BASE_URL
        self.LLM_MODEL_ID = LLM_MODEL_ID

    def run(self):
        try:
            if self.ollama_checkbox.isChecked():
                response = chat(model='minicpm-v:latest' if self.LLM_MODEL_ID is None else self.LLM_MODEL_ID, 
                                messages=self.memory)
                self.finished.emit(response['message']['content'])
            else:
                response = completion(
                    model="gemini/gemini-1.5-flash-002" if self.LLM_MODEL_ID is None else self.LLM_MODEL_ID,
                    base_url=None if self.AI_BASE_URL is None else self.AI_BASE_URL,
                    messages=self.memory,
                    api_key=None if self.LLM_API_MODEL is None else self.LLM_API_MODEL
                )
                self.finished.emit(response.choices[0].message.content)
        except Exception as e:
            self.error.emit(str(e))