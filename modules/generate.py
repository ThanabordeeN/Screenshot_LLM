from litellm import completion
from ollama import chat

class Generate():
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
                return response['message']['content'] , 200
            else:
                response = completion(
                    model=self.LLM_MODEL_ID if self.LLM_MODEL_ID is not None else None,
                    base_url=self.AI_BASE_URL if self.AI_BASE_URL is not None else None,
                    messages=self.memory,
                    api_key=self.LLM_API_MODEL if self.LLM_API_MODEL is not None else None
                )
        
            return response.choices[0].message.content , 200
        except Exception as e:
            raise e