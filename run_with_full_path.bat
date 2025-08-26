@echo off
title SPS Game - Run with Full ADB Path
color 0B

echo ==========================================
echo    SPS Game Automation
echo    Using Full ADB Path
echo ==========================================
echo.

:: Set ADB path
set ADB_PATH=D:\tools\platform-tools\adb.exe

:: Check if ADB exists
if not exist "%ADB_PATH%" (
    echo ❌ ADB not found at: %ADB_PATH%
    echo.
    echo Please run fix_adb_install.bat first!
    pause
    exit /b 1
)

echo ✅ Found ADB: %ADB_PATH%
echo.

:: Connect to MuMu12
echo 📱 Connecting to MuMu12...
"%ADB_PATH%" connect 127.0.0.1:16384
echo.

:: Check connection
echo 📋 Connected devices:
"%ADB_PATH%" devices
echo.

:: Activate virtual environment
echo 🐍 Activating Python environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, using global Python...
)

:: Modify the Python script to use full ADB path
echo.
echo 🚀 Running with modified ADB path...
python -c "import os; os.environ['ADB_PATH'] = r'D:\tools\platform-tools\adb.exe'; exec(open('quick_start.py').read())"

echo.
echo ==========================================
echo    Complete!
echo ==========================================
echo.
pause