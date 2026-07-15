@echo off
title Nexus Shopkeeper - Launcher
echo =======================================================================
echo   NEXUS SHOPKEEPER (PAKISTANI SAAS EDITION) - STARTUP UTILITY
echo =======================================================================
echo.

:: Detect Python executable (py vs python)
set PYTHON_EXE=
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_EXE=py
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_EXE=python
    )
)

if "%PYTHON_EXE%"=="" (
    echo [!] ERROR: Python was not found on your system PATH.
    echo Please install Python 3.9+ and check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo   [+] Python environment detected: %PYTHON_EXE%
echo   [+] Checking Python dependencies...
%PYTHON_EXE% -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo   [!] Warning: Dependency check returned non-zero code. Trying standard pip...
    pip install -r requirements.txt --quiet
)
echo   [+] Dependencies verified.
echo.
echo Launching FastAPI Backend Server...
echo.
start "Nexus Shopkeeper Backend" cmd /k "%PYTHON_EXE% -X utf8 backend\api_server.py"
echo   [+] Backend started in background.
echo.
echo Waiting 3 seconds for server to initialize...
timeout /t 3 /nobreak >nul
echo.
echo Opening Presentation Portal in your browser...
start http://localhost:8000/
echo.
echo =======================================================================
echo   Application launched! Keep the server command window open to shop.
echo   Press any key to close this launcher.
echo =======================================================================
pause >nul
