import PyInstaller.__main__
import os

# Get the absolute path to the icon
icon_path = os.path.abspath(os.path.join("assets", "icon.png"))

# PyInstaller arguments
args = [
    'game/snake.py',  # Main script
    '--onefile',  # Create a single executable
    '--noconsole',  # Don't show console window
    f'--icon={icon_path}',  # Set the icon
    '--name=SmartSnake',  # Name of the executable
    '--add-data=assets;assets',  # Include assets folder
    '--clean',  # Clean PyInstaller cache
]

# Run PyInstaller
PyInstaller.__main__.run(args) 