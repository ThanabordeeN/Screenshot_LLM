import os
import dotenv

def load_config():
    dotenv.load_dotenv()
    return {
        "LLM_API_KEY": os.getenv("LLM_API_KEY"),
        "BASE_URL": os.getenv("BASE_URL"),
        "LLM_MODEL_ID": os.getenv("LLM_MODEL_ID"),
        "OLLAMA": os.getenv("OLLAMA")
    }

def save_config(LLM_API_MODEL, AI_BASE_URL, LLM_MODEL_ID, OLLAMA):
    with open(".env", "w") as env_file:
        env_file.write(f"LLM_API_KEY={LLM_API_MODEL}\n")
        if AI_BASE_URL:
            env_file.write(f"BASE_URL={AI_BASE_URL}\n")
        if LLM_MODEL_ID:
            env_file.write(f"LLM_MODEL_ID={LLM_MODEL_ID}\n")
        if OLLAMA:
            env_file.write(f"OLLAMA=1\n")
    dotenv.load_dotenv(override=True)

def reset_config():
    with open(".env", "w") as env_file:
        env_file.write("")