#!/bin/bash


#!/bin/bash

# Path to your virtual environment's activation script
VENV_DIR="/home/graciano/Documents/Tempo-Foco-RLX/venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"

# Check if the activation script exists
if [ -f "$ACTIVATE_SCRIPT" ]; then
    # Source the activation script to activate the virtual environment
    source "$ACTIVATE_SCRIPT"
    echo "Virtual environment activated."
    cd $CRONO && python app.py
else
    echo "Error: Virtual environment not found or activation script does not exist."
fi


