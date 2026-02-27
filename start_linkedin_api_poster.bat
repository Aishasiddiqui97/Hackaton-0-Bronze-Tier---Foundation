@echo off
echo ========================================
echo LinkedIn API Autonomous Poster
echo ========================================
echo.
echo This will post all approved LinkedIn posts
echo from 03_Posted/History folder
echo.
pause

python linkedin_api_poster.py post

echo.
echo ========================================
echo Posting Complete!
echo ========================================
pause
