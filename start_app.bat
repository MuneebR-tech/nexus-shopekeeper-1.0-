@echo off
title Nexus Shopkeeper - Launcher
:: Force current working directory to the directory where start_app.bat is located
cd /d "%~dp0"

echo =======================================================================
echo   NEXUS SHOPKEEPER (PAKISTANI SAAS EDITION) - STARTUP UTILITY
echo =======================================================================
echo.

:: Verify project folders are extracted
if not exist "frontend\" (
    echo [!] ===================================================================
    echo [!] ERROR: MISSING PROJECT FOLDERS (frontend folder not found^)
    echo [!] ===================================================================
    echo [!] It looks like you ran start_app.bat directly inside the ZIP file,
    echo [!] or only extracted part of the project!
    echo [!]
    echo [!] Please right-click nexus_shopkeeper_submission.zip, select
    echo [!] "Extract All...", and run start_app.bat inside the EXTRACTED folder.
    echo [!] ===================================================================
    echo.
    pause
    exit /b 1
)

:: Detect Python executable (py vs python)
set PYTHON_EXE=
where py >nul 2>nul
if %errorlevel% equ 0 set PYTHON_EXE=py

if "%PYTHON_EXE%"=="" (
    where python >nul 2>nul
    if %errorlevel% equ 0 set PYTHON_EXE=python
)

if "%PYTHON_EXE%"=="" (
    echo [!] ERROR: Python was not found on your system PATH.
    echo Please install Python 3.8+ and check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Default port
set APP_PORT=8000
if exist .env (
    for /f "usebackq tokens=1,2 delims==" %%i in (".env") do (
        if "%%i"=="PORT" set APP_PORT=%%j
    )
)

echo   [+] Python environment detected: %PYTHON_EXE%
echo   [+] Checking core libraries (fastapi, uvicorn)...

%PYTHON_EXE% -c "import fastapi, uvicorn" >nul 2>nul
if %errorlevel% neq 0 (
    echo   [!] Core libraries missing. Installing requirements via pip...
    %PYTHON_EXE% -m pip install -r requirements.txt --user >nul 2>nul
    if %errorlevel% neq 0 (
        %PYTHON_EXE% -m pip install -r requirements.txt
    )
)

%PYTHON_EXE% -c "import fastapi, uvicorn" >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [!] ===================================================================
    echo [!] ERROR: MISSING PYTHON LIBRARIES (fastapi or uvicorn not installed^)
    echo [!] ===================================================================
    echo [!] We tried to install dependencies automatically, but pip failed
    echo [!] (possibly due to no internet connection or firewall rules on this PC^).
    echo [!]
    echo [!] Please open Command Prompt or Terminal and run:
    echo [!]     %PYTHON_EXE% -m pip install fastapi uvicorn pydantic python-dotenv
    echo [!] ===================================================================
    echo.
    pause
    exit /b 1
)

echo   [+] Dependencies verified.
echo.
echo Launching FastAPI Server...
echo Keep this command window OPEN while using the application!
echo.

:: Start background timer to open browser once server initializes and writes active_port.txt
start /b cmd /c "timeout /t 3 /nobreak >nul && (if exist data\active_port.txt (for /f "usebackq tokens=1 delims=" %%p in ("data\active_port.txt") do (if not "%%p"=="" set APP_PORT=%%p))) && start http://localhost:%APP_PORT%/"

:: Run server directly inside this primary window
%PYTHON_EXE% -X utf8 main.py

echo.
echo [!] Server stopped. Press any key to close launcher...
pause >nul
