@echo off
echo ========================================
echo Test All Social Media APIs
echo ========================================
echo.

echo [1/3] Testing Twitter API...
python api_twitter_poster.py "03_Posted\History\Twitter_Post_20260225_165309.md"
echo.
pause

echo.
echo [2/3] Testing Facebook API...
python api_facebook_poster.py "03_Posted\History\Facebook_Post_20260225_165309.md"
echo.
pause

echo.
echo [3/3] Testing LinkedIn (Playwright)...
python playwright_linkedin.py "03_Posted\History\POSTED_LinkedIn_Post_20260225_165309.md"
echo.

echo ========================================
echo All Tests Complete!
echo ========================================
pause
