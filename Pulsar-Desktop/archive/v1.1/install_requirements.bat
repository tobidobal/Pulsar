@echo off
setlocal
echo ==========================================
echo   Pulsar v1.1 - Requirements Installer
echo ==========================================
echo.
echo 1. Creating Virtual Environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo 2. Upgrading pip...
.\venv\Scripts\python.exe -m pip install --upgrade pip

echo 3. Installing requirements from requirements.txt...
.\venv\Scripts\pip.exe install -r requirements.txt

echo.
echo ==========================================
echo   DONE! Everything is ready.
echo   You can now run the program using 'run_pulsar.bat'.
echo ==========================================
pause
