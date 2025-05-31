#!/bin/bash

echo "Starting Snake Game..."
python3 game/snake.py

if [ $? -ne 0 ]; then
    echo "Error: Python or required packages not found."
    echo "Please make sure you have:"
    echo "1. Python installed"
    echo "2. Required packages installed (run: pip install -r requirements.txt)"
    read -p "Press Enter to continue..."
fi 