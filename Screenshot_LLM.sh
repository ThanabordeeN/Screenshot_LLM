#!/bin/bash
i=
# Define the lock file path
LOCKFILE="/tmp/screenshot_llm.lock"

# Define the virtual environment path
# Embed trailing slash to retain relative path capability
VENVPATH="${VENVPATH:-$HOME/.screenshot_llm/}"

# Function to pause the script
pause_script() {
    # Determine if executed via systemd unit
    if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
        echo "An error occurred. Pausing the script. Press [Enter] to continue..."
        rm "$LOCKFILE"
        read
    fi
    exit 1
}

# Prepare env file
if [[ -n "$SCRLLM_ENV_FILE" && ! -e "$SCRLLM_ENV_FILE" ]]; then
    [ ! -e "${SCRLLM_ENV_FILE%/*}" ] && mkdir -p "${SCRLLM_ENV_FILE%/*}"
    touch "$SCRLLM_ENV_FILE"
fi

# Check if the lock file exists
if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
    if [ -e "$LOCKFILE" ]; then
        echo "Another instance of the script is already running. Exiting."
        pause_script
    else
        # Create the lock file
        touch "$LOCKFILE"
    fi
fi

# Ensure the virtual environment is created and activated
if [ ! -d "${VENVPATH}venv" ]; then
    echo "Virtual environment not found. Creating one..."
    mkdir -p $VENVPATH
    python -m venv "${VENVPATH}venv"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        pause_script
    fi
fi

# Activate the virtual environment
source ${VENVPATH}venv/bin/activate

# Check if the virtual environment was activated successfully
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    pause_script
fi

# Install required Python packages if requirements.txt exists
if [ -f "requirements.txt" ]; then
    if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
        pip install -r requirements.txt > /dev/null 2>&1
    else
        # Log everything when executed via systemd
        pip install -r requirements.txt
    fi
    if [ $? -ne 0 ]; then
        echo "Failed to install required Python packages."
        pause_script
    fi
fi

# Check if the Python script is already running
if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
    if pgrep -f "python main.py --screenshot_llm" > /dev/null; then
        echo "Python script is already running. Exiting."
        rm "$LOCKFILE"
        exit 1
    fi
fi

# Run the main Python script in the background with nohup when run without systemd
# Send a bogus argument to match on to avoid conflicts managing the process
if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
    nohup python main.py --screenshot_llm > ${VENVPATH}/output.log 2>&1 &
else
    python main.py --screenshot_llm
fi

# Check if the script was started successfully when run without systemd
if [ -z "$SCRLLM_SYSTEMD_UNIT" ]; then
    if [ $? -eq 0 ]; then
        echo "Python script started successfully. Check 'output.log' for output."
        read -p "Press [Enter] to exit..."
    else
        echo "Failed to start the Python script."
        pause_script
    fi

    # The lock file will be removed automatically when the script exits
    trap "rm -f $LOCKFILE" EXIT
fi
