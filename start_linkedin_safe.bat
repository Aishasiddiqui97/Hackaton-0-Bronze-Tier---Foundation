@echo off
chcp 65001 >nul
echo ========================================
echo LinkedIn Safe Autonomous Poster
echo ========================================
echo.
echo This will start the Unicode-safe LinkedIn automation:
echo.
echo Features:
echo - Handles emojis and special characters safely
echo - Fixes ChromeDriver BMP limitations  
echo - Resolves Windows terminal encoding issues
echo - Uses JavaScript injection for reliability
echo - Multiple selector strategies for robustness
echo.
echo The system will:
echo 1. Monitor 03_Posted/History/ folder
echo 2. Auto-post LinkedIn files every 15 minutes
echo 3. Handle Unicode content safely
echo 4. Log all activities
echo.
pause

echo.
echo Starting LinkedIn Safe Autonomous Poster...
python autonomous_linkedin_safe.py

pause