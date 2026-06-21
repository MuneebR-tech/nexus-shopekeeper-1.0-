@echo off
echo =======================================================================
echo   NEXUS SHOPKEEPER - GITHUB PRIVATE REPOSITORY AUTOMATION
echo =======================================================================
echo.
echo GitHub deprecated password authentication in August 2021.
echo To push code, you must use a Personal Access Token (PAT).
echo.
echo HOW TO GENERATE A TOKEN:
echo 1. Open: https://github.com/settings/tokens in your browser.
echo 2. Click "Generate new token" -^> "Generate new token (classic)".
echo 3. Set note to "Nexus Shopkeeper" and check the [x] repo scope box.
echo 4. Click "Generate token" and COPY the token.
echo.
set /p TOKEN="Paste your GitHub Personal Access Token here: "
echo.
echo Staging latest changes...
git add .
git commit -m "Nexus Shopkeeper - Production Polish and Locators" 2>nul
echo.
echo Configuring remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/MuneebR-tech/nexus-shopkeeper.git
echo.
echo Pushing to private repository https://github.com/MuneebR-tech/nexus-shopkeeper.git...
git push -u https://MuneebR-tech:%TOKEN%@github.com/MuneebR-tech/nexus-shopkeeper.git main --force
echo.
echo =======================================================================
echo   Process complete. If you saw 'Branch main set up to track remote',
echo   your project has successfully uploaded to your private GitHub!
echo =======================================================================
echo.
pause
