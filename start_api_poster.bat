@echo off
echo ========================================
echo Autonomous API-Based Poster
echo ========================================
echo.
echo This uses official APIs (more reliable):
echo - LinkedIn: Playwright (browser)
echo - Twitter: API v2 (Bearer Token)
echo - Facebook: Graph API (Access Token)
echo.
echo Your credentials from .env:
echo - LinkedIn: ✅ Configured
echo - Twitter: ✅ API Token Available
echo - Facebook: ✅ API Token Available
echo.
pause

echo.
echo Starting API-based autonomous poster...
python autonomous_api_poster.py

pause
