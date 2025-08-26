@echo off
title SPS Game Automation - UV Setup
color 0A

echo ==========================================
echo    SPS Game Automation - Quick Setup
echo ==========================================
echo.

:: Check Python version
echo [Step 1] Checking Python version...
python --version 2>nul | findstr "3.11" >nul
if errorlevel 1 (
    echo ERROR: Python 3.11 not found!
    echo Please install Python 3.11.9 from python.org
    pause
    exit /b 1
)
python --version

:: Install UV
echo.
echo [Step 2] Installing UV package manager...
where uv >nul 2>nul
if errorlevel 1 (
    echo Installing UV...
    curl -LsSf https://astral.sh/uv/install.ps1 | powershell -
    if errorlevel 1 (
        echo Fallback: Installing UV via pip...
        pip install uv
    )
) else (
    echo UV already installed!
)

:: Create venv
echo.
echo [Step 3] Creating virtual environment...
if exist .venv (
    echo Virtual environment exists, removing old one...
    rmdir /s /q .venv
)
uv venv --python 3.11

:: Install dependencies
echo.
echo [Step 4] Installing dependencies...
call .venv\Scripts\activate.bat
uv pip install -r requirements-minimal.txt

:: Verify installation
echo.
echo [Step 5] Verifying installation...
python -c "import cv2, numpy, yaml, loguru; print('All packages OK!')"
if errorlevel 1 (
    echo ERROR: Package installation failed!
    pause
    exit /b 1
)

:: Check ADB
echo.
echo [Step 6] Checking ADB...
where adb >nul 2>nul
if errorlevel 1 (
    echo WARNING: ADB not found in PATH!
    echo Download from: https://developer.android.com/studio/releases/platform-tools
) else (
    echo ADB found!
    adb devices
)

:: Test MuMu12
echo.
echo ==========================================
echo    Testing MuMu12 Connection
echo ==========================================
echo.

:: Try to connect MuMu12
adb connect 127.0.0.1:16384 2>nul
timeout /t 2 >nul

:: Run test
python quick_start.py

echo.
echo ==========================================
echo    Setup Complete!
echo ==========================================
echo.
echo Commands:
echo   - Activate venv: .venv\Scripts\activate
echo   - Run main: python main.py
echo   - Test connection: python test_connection.py
echo.
pause