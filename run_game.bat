@echo off
echo Starting Smart Snake Game...
python game/snake.py
if errorlevel 1 (
    echo Error: Python or required packages not found.
    echo Please ensure Python is installed and run: pip install -r requirements.txt
    pause
) 