#!/bin/bash

# Define the lock file path
LOCKFILE="/tmp/screen_llm.lock"

# Function to pause the script
pause_script() {
    echo "An error occurred. Pausing the script. Press [Enter] to continue..."
    rm "$LOCKFILE"
    read
    exit 1
}

# Check if the lock file exists
if [ -e "$LOCKFILE" ]; then
    echo "Another instance of the script is already running. Exiting."
    pause_script
else
    # Create the lock file
    touch "$LOCKFILE"
fi

# Ensure the virtual environment is created and activated
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        pause_script
    fi
fi

# Activate the virtual environment
source venv/bin/activate

# Check if the virtual environment was activated successfully
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    pause_script
fi

# Install required Python packages if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Failed to install required Python packages."
        pause_script
    fi
fi

# Check if the Python script is already running
if pgrep -f "python main.py" > /dev/null; then
    echo "Python script is already running. Exiting."
    rm "$LOCKFILE"
    exit 1
fi

# Run the main Python script in the background with nohup
nohup python main.py > output.log 2>&1 &

# Check if the script was started successfully
if [ $? -eq 0 ]; then
    echo "Python script started successfully. Check 'output.log' for output."
    read -p "Press [Enter] to exit..."
else
    echo "Failed to start the Python script."
    pause_script
fi

# The lock file will be removed automatically when the script exits
trap "rm -f $LOCKFILE" EXIT
