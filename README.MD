# Screenshot LLM

Screenshot LLM is a Python application that utilizes PyQt5 for the user interface and integrates with various AI models to analyze screenshots. The application allows users to interact with screenshots and receive insights based on the content of the images.

## Features

- **Screenshot Detection**: Automatically detects new screenshots saved in the user's designated screenshot directory.
- **User Interface**: A clean and intuitive interface built with PyQt5, allowing users to interact with the application easily.
- **Configuration Management**: Users can configure API keys and model IDs through the settings tab.
- **Memory Management**: The application can reset its memory and configurations as needed.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure you have the necessary API keys for the AI models you wish to use.
2. Run the application using the following command:

```bash
python main.py
```

3. The application will start, and you can interact with it through the GUI.

## Configuration

The application uses a `.env` file to store configuration settings. You can set the following variables:

- `LLM_API_KEY`: Your API key for the LLM service.
- `BASE_URL`: (Optional) The base URL for the API.
- `LLM_MODEL_ID`: (Optional) The model ID to use for the LLM.
- `OLLAMA`: (Optional) Set to `1` to enable Ollama integration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [python-dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables.
- [litellm](https://pypi.org/project/litellm/) for AI model integration.
- [ollama](https://github.com/ollama/ollama-python) for Local LLM Inference 
