@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
python build_exe.py

echo.
echo If the build was successful, you can find the executable in the 'dist' folder.
echo.
pause 