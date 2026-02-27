@echo off
echo ========================================
echo Fix Issues and Push to GitHub
echo ========================================
echo.

echo [1/5] Deleting files with long names...
del /F /Q "00_Inbox\WhatsApp\test_message_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED_REPLIED.md" 2>nul
del /F /Q "00_Inbox\WhatsApp\test_message_*.md" 2>nul
echo Done!

echo.
echo [2/5] Cleaning up unnecessary files...
del /F /Q "Untitled*.canvas" 2>nul
del /F /Q "Untitled*.base" 2>nul
del /F /Q "*.json" 2>nul
del /F /Q "config.c" 2>nul
echo Done!

echo.
echo [3/5] Adding all files...
git add .

echo.
echo [4/5] Committing changes...
git commit -m "Gold Tier Complete: Autonomous LinkedIn posting system with anti-detection and Unicode safety"

echo.
echo [5/5] Pushing to GitHub...
echo Checking internet connection...
ping github.com -n 1 >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Cannot connect to GitHub!
    echo.
    echo Please check:
    echo 1. Internet connection
    echo 2. VPN if required
    echo 3. Firewall settings
    echo.
    echo Try again after fixing connection.
    pause
    exit /b 1
)

git push origin main

echo.
echo ========================================
echo Push Complete!
echo ========================================
echo.
echo Repository: https://github.com/Aishasiddiqui97/Hackaton-0
echo.
pause
