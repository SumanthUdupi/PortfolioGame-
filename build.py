#!/usr/bin/env python3
"""
Build script for creating a standalone executable of Pixel Art RPG Portfolio using PyInstaller.
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the standalone executable for Windows distribution."""

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Clean previous build
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window
        "--name", "Pixel_Art_RPG_Portfolio",
        "--add-data", f"assets{os.pathsep}assets",  # Include assets directory
        "--add-data", f"config.py{os.pathsep}.",  # Include config file
        "--add-data", f"savegame.json{os.pathsep}.",  # Include save file
        "--hidden-import", "pygame",
        "--hidden-import", "pygame_gui",
        "--hidden-import", "pytmx",
        "--hidden-import", "PIL",
        "--hidden-import", "numpy",
        "--hidden-import", "jsonschema",
        "main.py"
    ]

    print("Building executable...")
    subprocess.check_call(cmd)

    print("Build completed successfully!")
    print(f"Executable created at: {os.path.join('dist', 'Pixel_Art_RPG_Portfolio.exe')}")

if __name__ == "__main__":
    build_executable()