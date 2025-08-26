# PowerShell script to setup and run with UV

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SPS Game Automation - UV Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install UV
Write-Host "[1/6] Installing UV..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing UV package manager..." -ForegroundColor Gray
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    # Add to PATH for current session
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
} else {
    Write-Host "UV already installed ✓" -ForegroundColor Green
}

# Step 2: Navigate to project directory
Write-Host ""
Write-Host "[2/6] Setting project directory..." -ForegroundColor Yellow
Set-Location -Path "D:\pyproject\sps-game-automation"
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Gray

# Step 3: Create virtual environment
Write-Host ""
Write-Host "[3/6] Creating Python 3.11 virtual environment..." -ForegroundColor Yellow
uv venv --python 3.11
if ($LASTEXITCODE -eq 0) {
    Write-Host "Virtual environment created ✓" -ForegroundColor Green
} else {
    Write-Host "Failed to create venv!" -ForegroundColor Red
    exit 1
}

# Step 4: Install dependencies
Write-Host ""
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow
uv pip install -r requirements-minimal.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed ✓" -ForegroundColor Green
} else {
    Write-Host "Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

# Step 5: Test imports
Write-Host ""
Write-Host "[5/6] Testing imports..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe -c @"
import cv2
import numpy as np
import yaml
import loguru
print('✅ All modules imported successfully!')
print(f'  OpenCV: {cv2.__version__}')
print(f'  NumPy: {np.__version__}')
"@

# Step 6: Run connection test
Write-Host ""
Write-Host "[6/6] Testing MuMu12 connection..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Check if MuMu12 is running
$adbDevices = & adb devices 2>$null
if ($adbDevices -match "127.0.0.1:16384") {
    Write-Host "MuMu12 detected! Running test..." -ForegroundColor Green
    .\.venv\Scripts\python.exe quick_start.py
} else {
    Write-Host "⚠️  MuMu12 not detected!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please ensure:" -ForegroundColor White
    Write-Host "1. MuMu12 emulator is running" -ForegroundColor Gray
    Write-Host "2. USB debugging is enabled in MuMu12 settings" -ForegroundColor Gray
    Write-Host "3. Try running: adb connect 127.0.0.1:16384" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Running connection test anyway..." -ForegroundColor Yellow
    .\.venv\Scripts\python.exe test_connection.py
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate venv manually:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "To run the main program:" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan