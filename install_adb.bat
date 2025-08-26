@echo off
title Install ADB for Windows
color 0E

echo ==========================================
echo    Installing ADB (Android Debug Bridge)
echo ==========================================
echo.

:: Create tools directory
echo [1/4] Creating tools directory...
if not exist "D:\tools" mkdir D:\tools
cd /d D:\tools

:: Download platform-tools
echo.
echo [2/4] Downloading Android Platform Tools...
echo This may take a minute...
curl -L -o platform-tools.zip https://dl.google.com/android/repository/platform-tools-latest-windows.zip
if errorlevel 1 (
    echo ERROR: Download failed!
    echo.
    echo Please download manually from:
    echo https://developer.android.com/studio/releases/platform-tools
    echo.
    echo Extract to: D:\tools\platform-tools
    pause
    exit /b 1
)

:: Extract
echo.
echo [3/4] Extracting files...
powershell -Command "Expand-Archive -Path platform-tools.zip -DestinationPath . -Force"
del platform-tools.zip

:: Add to PATH
echo.
echo [4/4] Adding to system PATH...
setx PATH "%PATH%;D:\tools\platform-tools" /M 2>nul
if errorlevel 1 (
    echo Need admin rights to add to system PATH.
    echo Adding to user PATH instead...
    setx PATH "%PATH%;D:\tools\platform-tools"
)

:: Test ADB
echo.
echo ==========================================
echo    Testing ADB Installation
echo ==========================================
D:\tools\platform-tools\adb.exe version
echo.

:: Try connecting to MuMu12
echo Attempting to connect to MuMu12...
D:\tools\platform-tools\adb.exe connect 127.0.0.1:16384
D:\tools\platform-tools\adb.exe devices

echo.
echo ==========================================
echo    Installation Complete!
echo ==========================================
echo.
echo ADB is installed at: D:\tools\platform-tools\adb.exe
echo.
echo IMPORTANT: Close this window and open a NEW command prompt
echo for the PATH changes to take effect!
echo.
echo Then run: setup_and_run.cmd again
echo.
pause