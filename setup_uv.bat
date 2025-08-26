@echo off
echo ========================================
echo UV Setup for SPS Game Automation
echo ========================================
echo.

REM Install uv if not installed
echo [1/5] Installing UV package manager...
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
if errorlevel 1 (
    echo Failed to install UV, trying pip...
    pip install uv
)

echo.
echo [2/5] Creating virtual environment with Python 3.11...
uv venv --python 3.11

echo.
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/5] Installing dependencies...
uv pip install -r requirements-minimal.txt

echo.
echo [5/5] Verifying installation...
python -c "import cv2; import numpy; import yaml; print('✅ All packages installed successfully!')"

echo.
echo ========================================
echo Setup complete! 
echo.
echo To test MuMu12 connection:
echo   python quick_start.py
echo.
echo To activate venv later:
echo   .venv\Scripts\activate
echo ========================================
pause