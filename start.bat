@echo off
REM Quick start script for TikTok Bot Web Application (Windows)

echo 🚀 Starting TikTok Bot Web Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

REM Create Data directory
if not exist "Data" (
    echo 📁 Creating Data directory...
    mkdir Data
)

REM Create empty Proxies.txt if it doesn't exist
if not exist "Data\Proxies.txt" (
    echo 📝 Creating Proxies.txt...
    type nul > Data\Proxies.txt
    echo ⚠️  Please add proxies to Data\Proxies.txt (one per line)
)

REM Count proxies
for /f %%A in ('type "Data\Proxies.txt" ^| find /c /v ""') do set PROXY_COUNT=%%A
if "%PROXY_COUNT%"=="0" (
    echo ⚠️  WARNING: No proxies found in Data\Proxies.txt
    echo    Add proxies before starting the bot for best results
) else (
    echo ✅ Found %PROXY_COUNT% proxies
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎉 TikTok Bot Web Application is starting...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📡 Web Interface: http://localhost:5000
echo 🔧 API Health: http://localhost:5000/health
echo.
echo Press Ctrl+C to stop the server
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Run the application
python web_app.py

pause
