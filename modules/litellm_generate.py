from litellm import completion


from PyQt5.QtCore import QThread, pyqtSignal


class Worker_litellm(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, memory, LLM_API_MODEL, LLM_MODEL_ID):
        super().__init__()
        self.memory = memory
        self.LLM_API_MODEL = LLM_API_MODEL
        self.LLM_MODEL_ID = LLM_MODEL_ID
        
    def run(self):
        try:
            response = completion(
                model=self.LLM_MODEL_ID if self.LLM_MODEL_ID is not None else None,
                messages=self.memory,
                api_key=self.LLM_API_MODEL if self.LLM_API_MODEL is not None else None
            )
            self.finished.emit(response.choices[0].message.content)
        except Exception as e:
            self.error.emit(str(e))