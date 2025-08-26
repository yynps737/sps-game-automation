@echo off
title Fix ADB Installation
color 0A

echo ==========================================
echo    Fixing ADB Installation
echo ==========================================
echo.

cd /d D:\tools

:: Check if zip file exists
if exist platform-tools.zip (
    echo Found platform-tools.zip, extracting...
    
    :: Method 1: Try using tar (Windows 10+ has it)
    tar -xf platform-tools.zip 2>nul
    if errorlevel 1 (
        echo tar failed, trying alternative method...
        
        :: Method 2: Try using PowerShell.exe with full path
        C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -Command "Expand-Archive -Path platform-tools.zip -DestinationPath . -Force" 2>nul
        
        if errorlevel 1 (
            echo.
            echo ERROR: Cannot extract automatically.
            echo Please extract platform-tools.zip manually to D:\tools\
            echo You can use 7-Zip or Windows Explorer
            explorer.exe D:\tools
            pause
            exit /b 1
        )
    )
    
    del platform-tools.zip 2>nul
    echo Extraction complete!
) else (
    echo platform-tools.zip not found, checking if already extracted...
)

:: Verify ADB exists
if not exist "D:\tools\platform-tools\adb.exe" (
    echo.
    echo ERROR: adb.exe not found at D:\tools\platform-tools\
    echo.
    echo Please:
    echo 1. Download platform-tools manually from:
    echo    https://dl.google.com/android/repository/platform-tools-latest-windows.zip
    echo 2. Extract it to D:\tools\
    echo 3. Make sure D:\tools\platform-tools\adb.exe exists
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ ADB found at: D:\tools\platform-tools\adb.exe
echo.

:: Test ADB directly
echo Testing ADB...
D:\tools\platform-tools\adb.exe version
echo.

:: Connect to MuMu12
echo Connecting to MuMu12...
D:\tools\platform-tools\adb.exe connect 127.0.0.1:16384
echo.

:: Show devices
echo Listing devices...
D:\tools\platform-tools\adb.exe devices
echo.

echo ==========================================
echo    Setup Complete!
echo ==========================================
echo.
echo ADB is working at: D:\tools\platform-tools\adb.exe
echo.
echo To use ADB from anywhere, add to PATH:
echo   D:\tools\platform-tools
echo.
echo You can now:
echo 1. Close this window
echo 2. Open a NEW command prompt
echo 3. Run: D:\pyproject\sps-game-automation\setup_and_run.cmd
echo.
pause