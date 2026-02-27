@echo off
echo ========================================
echo Autonomous Social Media Poster
echo ========================================
echo.
echo This will:
echo - Monitor 03_Posted/History folder
echo - Auto-post to LinkedIn, Twitter, Facebook
echo - Check every 15 minutes
echo - Run continuously (Ctrl+C to stop)
echo.
echo Make sure you have:
echo 1. Run setup_playwright.bat
echo 2. Added credentials to .env file
echo.
pause

echo.
echo Starting autonomous poster...
python autonomous_poster.py

pause
