@echo off
title Nexus Shopkeeper - Launcher
echo =======================================================================
echo   NEXUS SHOPKEEPER (PAKISTANI SAAS EDITION) - STARTUP UTILITY
echo =======================================================================
echo.
echo Checking Python dependencies...
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo   [!] Warning: Dependency check returned non-zero code. Trying standard pip...
    pip install -r requirements.txt --quiet
)
echo   [+] Dependencies verified.
echo.
echo Launching FastAPI Backend Server...
echo.
start "Nexus Shopkeeper Backend" cmd /k "py -X utf8 backend\api_server.py"
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
