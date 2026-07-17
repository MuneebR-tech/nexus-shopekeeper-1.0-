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

:: Detect Python executable (py vs python vs python3)
set PYTHON_EXE=
where py >nul 2>nul
if %errorlevel% equ 0 set PYTHON_EXE=py

if "%PYTHON_EXE%"=="" (
    where python >nul 2>nul
    if %errorlevel% equ 0 set PYTHON_EXE=python
)

if "%PYTHON_EXE%"=="" (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 set PYTHON_EXE=python3
)

:: If still not found on PATH, automatically scan all common Windows installation directories
if "%PYTHON_EXE%"=="" (
    for %%p in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
        "C:\Python310\python.exe"
        "C:\Python39\python.exe"
        "C:\Python38\python.exe"
        "C:\Program Files\Python312\python.exe"
        "C:\Program Files\Python311\python.exe"
        "C:\Program Files\Python310\python.exe"
        "C:\Program Files\Python39\python.exe"
        "C:\Program Files\Python38\python.exe"
        "C:\Anaconda3\python.exe"
        "C:\ProgramData\Anaconda3\python.exe"
        "%USERPROFILE%\Anaconda3\python.exe"
        "%USERPROFILE%\Miniconda3\python.exe"
        "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    ) do (
        if exist %%p (
            if "%PYTHON_EXE%"=="" set PYTHON_EXE=%%p
        )
    )
)

if "%PYTHON_EXE%"=="" (
    echo.
    echo [!] ===================================================================
    echo [!] WARNING: Python was not found on your system PATH or standard folders.
    echo [!] ===================================================================
    echo [!] If Python IS installed on this PC in a custom location, please type
    echo [!] or paste the exact full path to python.exe below and press Enter
    echo [!] (for example: C:\Users\YourName\Python\python.exe^)
    echo [!]
    echo [!] If Python is NOT installed on this PC yet, press Enter to exit,
    echo [!] download Python from https://python.org/downloads/ and check the
    echo [!] "Add Python to PATH" box during installation!
    echo [!] ===================================================================
    echo.
    set /p PYTHON_EXE="Enter full path to python.exe (or press Enter to exit): "
)

if "%PYTHON_EXE%"=="" (
    echo [!] No Python executable provided. Exiting launcher.
    pause
    exit /b 1
)

:: Clean up quotes if user pasted path with surrounding quotes
set PYTHON_EXE=%PYTHON_EXE:"=%
if not exist "%PYTHON_EXE%" (
    where %PYTHON_EXE% >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] ERROR: Could not locate python executable at "%PYTHON_EXE%".
        pause
        exit /b 1
    )
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
