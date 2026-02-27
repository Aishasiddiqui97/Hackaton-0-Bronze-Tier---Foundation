@echo off
echo ========================================
echo Setup Twitter OAuth 1.0a
echo ========================================
echo.
echo Installing Tweepy library for proper
echo Twitter OAuth 1.0a authentication...
echo.
pause

pip install tweepy

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Your Twitter credentials in .env:
echo - API_KEY: ✅
echo - API_SECRET: ✅
echo - ACCESS_TOKEN: ✅
echo - ACCESS_TOKEN_SECRET: ✅
echo.
echo Test with:
echo   python fix_twitter_oauth.py
echo.
pause
