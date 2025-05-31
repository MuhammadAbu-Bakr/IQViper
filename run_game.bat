@echo off
echo Starting Snake Game...
python game/snake.py
if errorlevel 1 (
    echo Error: Python or required packages not found.
    echo Please make sure you have:
    echo 1. Python installed
    echo 2. Required packages installed (run: pip install -r requirements.txt)
    pause
) 