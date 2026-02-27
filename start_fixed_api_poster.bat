@echo off
echo ========================================
echo Autonomous API Poster (Fixed OAuth)
echo ========================================
echo.
echo This uses proper authentication:
echo - LinkedIn: Playwright
echo - Twitter: OAuth 1.0a (Tweepy)
echo - Facebook: Graph API
echo.
echo Setup required:
echo 1. Run: setup_twitter_oauth.bat
echo 2. Fix Facebook token (see fix_facebook_token.md)
echo.
pause

echo.
echo Starting fixed API poster...
python autonomous_api_fixed.py

pause
