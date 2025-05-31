@echo off
echo Installing PyInstaller if not already installed...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed --name "SnakeGame" game/snake.py

echo.
echo If build was successful, you can find the executable in the 'dist' folder.
echo.
pause 