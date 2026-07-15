@echo off
title Nexus Shopkeeper - Launcher
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
)
if "%PYTHON_EXE%"=="" (
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

:: Parse .env file for PORT configuration
if exist .env (
    for /f "usebackq tokens=1,2 delims==" %%i in (".env") do (
        if "%%i"=="PORT" (
            set APP_PORT=%%j
        )
    )
)

echo   [+] Python environment detected: %PYTHON_EXE%
echo   [+] Target application port: %APP_PORT%
echo   [+] Checking Python dependencies...
%PYTHON_EXE% -m pip install -r requirements.txt --user >nul 2>nul
if %errorlevel% neq 0 (
    echo   [!] Retrying dependency installation without --user flag...
    %PYTHON_EXE% -m pip install -r requirements.txt
)
if %errorlevel% neq 0 (
    pip install -r requirements.txt --user
)
echo   [+] Dependencies verified.
echo.
echo Launching FastAPI Backend Server...
echo.
start "Nexus Shopkeeper Backend" cmd /k "%PYTHON_EXE% -X utf8 backend\api_server.py"
echo   [+] Backend started in background.
echo.
echo Waiting 4 seconds for server to initialize and bind port...
timeout /t 4 /nobreak >nul
echo.
if exist "data\active_port.txt" (
    for /f "usebackq tokens=1 delims=" %%p in ("data\active_port.txt") do (
        if not "%%p"=="" set APP_PORT=%%p
    )
)
echo Opening Presentation Portal on verified port http://localhost:%APP_PORT%/ ...
start http://localhost:%APP_PORT%/
echo.
echo =======================================================================
echo   Application launched! Keep the server command window open to shop.
echo   Press any key to close this launcher.
echo =======================================================================
pause >nul
