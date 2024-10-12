# Screenshot LLM: AI-Powered Screenshot Analysis

Screenshot LLM is a Python application that leverages the power of AI to analyze screenshots.  Built with PyQt5 for a user-friendly interface and integrating with various AI models (including Ollama), it provides insightful information directly from images.

## Features

* **Automated Screenshot Detection:** Automatically detects new screenshots saved in a user-specified directory.
* **Intuitive PyQt5 GUI:**  A clean and easy-to-use graphical interface for seamless interaction.
* **Configurable AI Models:** Supports multiple AI models via configurable API keys and model IDs.
* **Flexible Configuration:**  Manage settings, including API keys and model selection, through a dedicated settings tab.
* **Memory Management:**  Allows resetting application memory and configurations.
* **Ollama Integration (Optional):**  Analyze screenshots using your local Ollama models.


## Getting Started

**Pre-built Executable:**

For a quick start, download the pre-built executable:

[Download](https://drive.google.com/file/d/1RTobs3usu4oucYrTiEIHWD84KjNASXWw/view?usp=sharing)

1. Extract the downloaded zip file.
2. Run `Screenshot_LLM.exe`.


## Installation Instructions for Linux Users

1. **Make the `Screenshot_LLM` script executable:**

    ```sh
    chmod +x Screenshot_LLM.sh
    ```

2. **Run the `Screenshot_LLM` script through the terminal:**

    ```sh
    Screenshot_LLM.sh
    ```

These steps will ensure that the `Installer.sh` script is executable, the necessary environment variables are set, and the `Screenshot_LLM` script can be run from any terminal session.

**From Source Code:**

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:** Create a `.env` file in the project's root directory and add your API keys and settings:

   ```
   LLM_API_KEY=YOUR_API_KEY  # Your API key for the LLM
   LLM_MODEL_ID=your_model_id  # (Optional) Your preferred model ID
   OLLAMA=1  # Set to 1 to enable Ollama integration (requires Ollama to be running)
   SCREENSHOT_DIRECTORY=C:/path/to/your/screenshots  # Path to your screenshot directory.  Defaults to standard location if not provided.
   ```

3. **Run the Application:**

   ```bash
   python main.py
   ```

## Usage

1.  Provide your API keys and configure settings in the `.env` file or the application's settings tab.
2.  Run the application.  It will monitor your designated screenshot directory.
3.  New screenshots will be automatically processed and analyzed, providing insights via the user interface.


## Configuration Details

The application uses a `.env` file to store configuration details.  Essential settings include:

*   `LLM_API_KEY`: Your API key for the chosen LLM service.
*   `LLM_MODEL_ID`: (Optional) The specific model ID to utilize.
*   `OLLAMA`: (Optional) Set to `1` to enable local LLM inference using Ollama.  Requires Ollama to be running and configured.
*   `SCREENSHOT_DIRECTORY`: [Optional] Path to the directory containing screenshots.


## License

This project is licensed under the MIT License.  See the `LICENSE` file for details.


## Acknowledgments

*   **PyQt5:** For the user interface.
*   **python-dotenv:** For environment variable management.
*   **litellm:** For AI model integration.
*   **ollama:** For local LLM inference (optional).


This revised description is clearer, more concise, and better organized for readability.  It also provides more specific guidance for setup and usage.
