# Screenshot Analyzer

## Overview
Screenshot Analyzer is a desktop application built using PyQt5 that allows users to analyze screenshots. The application leverages a language model to provide insights and answers based on the content of the screenshots.

## Features
- Display screenshots in a user-friendly interface.
- Interact with an AI assistant to ask questions about the displayed screenshot.
- Save and reset configurations for the AI model.
- Monitor the user's screenshot directory for new images.

## Installation

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Dependencies
Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Set up your environment variables in a `.env` file or directly in the application settings.
4. Run the application:

```bash
python main.py
```

5. The application will start, and you can interact with it by asking questions about the displayed screenshot.

## Configuration
The application requires the following environment variables to be set in a `.env` file:

- `LLM_API_KEY`: Your API key for the language model.
- `BASE_URL`: (Optional) The base URL for the AI service.
- `LLM_MODEL_ID`: (Optional) The model ID to use for the AI service.

## Screenshot Directory
The application monitors the default screenshot directory, which is typically located at:
- `C:\Users\<YourUsername>\Pictures\Screenshots`

You can change this directory in the `screenshot_watcher.py` file if needed.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [litellm](https://github.com/yourusername/litellm) for the language model integration.
