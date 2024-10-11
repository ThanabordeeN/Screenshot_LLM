# Screenshot Analyzer

This project is a screenshot analyzer application built using PyQt5. It allows users to analyze screenshots and interact with an AI model to ask questions about the screenshot.

## Features

- Display screenshots
- Interactive conversation area
- AI-based question answering about the screenshot

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables:
        ```
        LLM_API_KEY=<your-llm-api-key>
        BASE_URL=<your-base-url>
        ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. The application will open a window where you can load and analyze screenshots.

## Project Structure

- [`main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fcepheusn22%2FDocuments%2FPython_Projects%2Fscreenshort_llm%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22edc96558-2e6c-4c34-b516-d34d9ec49f03%22%5D "/home/cepheusn22/Documents/Python_Projects/screenshort_llm/main.py"): The main entry point of the application.
- [`interface.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fcepheusn22%2FDocuments%2FPython_Projects%2Fscreenshort_llm%2Finterface.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22edc96558-2e6c-4c34-b516-d34d9ec49f03%22%5D "/home/cepheusn22/Documents/Python_Projects/screenshort_llm/interface.py"): The generated UI class from the Qt Designer `.ui` file.
- [`interface.ui`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fcepheusn22%2FDocuments%2FPython_Projects%2Fscreenshort_llm%2Finterface.ui%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22edc96558-2e6c-4c34-b516-d34d9ec49f03%22%5D "/home/cepheusn22/Documents/Python_Projects/screenshort_llm/interface.ui"): The Qt Designer file for the UI layout.
- [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fcepheusn22%2FDocuments%2FPython_Projects%2Fscreenshort_llm%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22edc96558-2e6c-4c34-b516-d34d9ec49f03%22%5D "/home/cepheusn22/Documents/Python_Projects/screenshort_llm/.env"): Environment variables file (not included in the repository).

## License

This project is licensed under the MIT License.