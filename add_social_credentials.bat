@echo off
echo ========================================
echo Add Social Media Credentials
echo ========================================
echo.
echo Current .env file will be updated with
echo Twitter and Facebook credentials.
echo.
echo LinkedIn is already configured:
echo   Email: aishaanjumsiddiqui97@gmail.com
echo.
pause

echo.
echo Opening .env file in notepad...
echo.
echo Please add your credentials:
echo.
echo For Twitter/X:
echo   TWITTER_EMAIL=your_email@gmail.com
echo   TWITTER_USERNAME=your_username
echo   TWITTER_PASSWORD=your_password
echo.
echo For Facebook:
echo   FACEBOOK_EMAIL=your_email@gmail.com
echo   FACEBOOK_PASSWORD=your_password
echo.
echo Save and close notepad when done.
echo.
pause

notepad .env

echo.
echo ========================================
echo Credentials Updated!
echo ========================================
echo.
echo Next steps:
echo 1. Restart autonomous poster if running
echo 2. Test individual platforms:
echo    python playwright_twitter.py
echo    python playwright_facebook.py
echo.
pause
