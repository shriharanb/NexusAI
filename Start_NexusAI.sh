#!/bin/bash

# 1. Dynamically get the folder where this script is saved
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 2. Activate your Python virtual environment safely
if [ -f "NexusEnv/bin/activate" ]; then
    source NexusEnv/bin/activate
else
    echo "Error: Virtual environment (venv) not found in $SCRIPT_DIR"
    exit 1
fi

# 3. Launch your main application entry point script
python3 main.py