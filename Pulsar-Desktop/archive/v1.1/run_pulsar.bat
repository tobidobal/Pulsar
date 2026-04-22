@echo off
if not exist venv (
    echo [ERROR] Virtual environment not found. 
    echo Please run 'install_requirements.bat' first.
    pause
    exit /b
)
echo Starting Pulsar v1.1...
start "" /B .\venv\Scripts\pythonw.exe main.py
