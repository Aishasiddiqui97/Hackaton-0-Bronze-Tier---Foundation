@echo off
chcp 65001 >nul
echo ========================================
echo LinkedIn Unicode Safe Posting Test
echo ========================================
echo.
echo This will:
echo 1. Create a Unicode test post with emojis
echo 2. Post it safely to LinkedIn
echo 3. Handle all encoding issues automatically
echo.
echo Features:
echo - ChromeDriver BMP compatibility
echo - Windows terminal encoding fix
echo - JavaScript injection method
echo - Multiple selector strategies
echo.
pause

echo.
echo Creating Unicode test post...
python test_linkedin_unicode.py

echo.
echo Posting to LinkedIn with Unicode safety...
python linkedin_selenium_fixed.py

echo.
echo Test complete!
pause