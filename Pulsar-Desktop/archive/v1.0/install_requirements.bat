@echo off
setlocal
echo ==========================================
echo   Pulsar v1.0 - Requirements Installer
echo ==========================================
echo.

echo 1. Creating Virtual Environment...
if exist venv ( rd /s /q venv )
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    pause
    exit /b
)

echo 2. Installing requirements...
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\pip.exe install -r requirements.txt --quiet

echo 3. Checking for FFmpeg (Auto-setup)...
if not exist "bin\ffmpeg.exe" (
    echo    FFmpeg not found. Downloading essentials...
    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'; $zip = 'ffmpeg.zip'; Invoke-WebRequest -Uri $url -OutFile $zip; Expand-Archive $zip -DestinationPath 'ffmpeg_temp' -Force; if (Test-Path 'ffmpeg_temp') { $bin = Get-ChildItem -Path 'ffmpeg_temp' -Filter 'ffmpeg.exe' -Recurse | Select-Object -First 1; $dir = $bin.Directory.FullName; New-Item -ItemType Directory -Force 'bin' | Out-Null; Copy-Item \"$dir\*.exe\" -Destination 'bin' -Force; Remove-Item -Recurse -Force 'ffmpeg_temp'; Remove-Item -Force $zip; } }"
)

echo.
echo DONE! Run the app with 'run_Pulsar_v1.0.bat'.
pause
