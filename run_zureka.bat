@echo off
setlocal enabledelayedexpansion
title Zureka Solutions - Python Enterprise Desk
cd /d "%~dp0"

echo ======================================================================
echo          ZUREKA SOLUTIONS LIMITED - ENTERPRISE SYSTEMS DESK
echo      "Building Better Businesses. Together." - Kampala, Uganda
echo      100%% Offline Python Backend ^| Pandora Networks SMS Gateway
echo ======================================================================
echo.

set "PY_EXE="

:: 1. Check exact Python 3.15 installation path
if exist "%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe"
    goto :FoundPython
)

:: 2. Check standard Python in Programs folder
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :FoundPython
    )
)

:: 3. Check Program Files
for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXE=%%D\python.exe"
        goto :FoundPython
    )
)

:: 4. Try py launcher
where py.exe >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_EXE=py"
    goto :FoundPython
)

:: 5. Try default python command
where python.exe >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_EXE=python"
    goto :FoundPython
)

:FoundPython
if "%PY_EXE%"=="" (
    echo [ERROR] Python was not found on your system!
    echo Please install Python 3.10+ or check your installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Using Python: %PY_EXE%
echo.
echo Launching web browser at http://localhost:8080 ...
start "" "http://localhost:8080"
echo.
echo Starting Zureka Solutions Python backend on port 8080...
echo Leave this window OPEN while working in the Desk.
echo Press Ctrl+C to stop the server.
echo ======================================================================
echo.

"%PY_EXE%" app.py

echo.
echo ======================================================================
echo Server stopped.
echo ======================================================================
pause
