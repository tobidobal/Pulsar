@echo off
setlocal
echo ==========================================
echo   Pulsar v1.2 - Requirements Installer
echo ==========================================
echo.

echo 1. Checking for Virtual Environment...
if exist venv (
    echo    Found old venv - removing to ensure clean install...
    rd /s /q venv 2>nul
)
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b
)

echo 2. Installing Python libraries...
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\pip.exe install -r requirements.txt --quiet

echo 3. Checking for FFmpeg (Auto-setup)...
if not exist "bin\ffmpeg.exe" (
    echo    FFmpeg not found. Downloading essentials (approx. 90MB)...
    echo    This may take a minute depending on your connection...
    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'; $zip = 'ffmpeg.zip'; Invoke-WebRequest -Uri $url -OutFile $zip; Expand-Archive $zip -DestinationPath 'ffmpeg_temp' -Force; if (Test-Path 'ffmpeg_temp') { $bin = Get-ChildItem -Path 'ffmpeg_temp' -Filter 'ffmpeg.exe' -Recurse | Select-Object -First 1; $dir = $bin.Directory.FullName; Copy-Item \"$dir\*.exe\" -Destination 'bin' -Force; Remove-Item -Recurse -Force 'ffmpeg_temp'; Remove-Item -Force $zip; } }"
    if exist "bin\ffmpeg.exe" (
        echo    FFmpeg installed successfully in \bin folder.
    ) else (
        echo    [WARN] Auto-download failed. Please install FFmpeg manually.
    )
) else (
    echo    FFmpeg is already present.
)

echo.
echo ==========================================
echo   DONE! Everything is ready.
echo   You can now run the program using 'run_Pulsar_v1.2.bat'.
echo ==========================================
pause
