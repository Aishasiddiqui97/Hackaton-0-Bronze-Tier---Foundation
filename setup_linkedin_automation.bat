@echo off
echo ========================================
echo LinkedIn Automation Setup
echo ========================================
echo.
echo This will install required packages for
echo LinkedIn browser automation (no API needed)
echo.
pause

echo.
echo [1/2] Installing Selenium...
pip install selenium

echo.
echo [2/2] Installing WebDriver Manager...
pip install webdriver-manager

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure Chrome browser is installed
echo 2. Your LinkedIn credentials are in .env file
echo 3. Run: python linkedin_auto_poster.py
echo.
echo To test posting:
echo   python linkedin_auto_poster.py "03_Posted\History\LinkedIn_Post_20260225_165309.md"
echo.
pause
