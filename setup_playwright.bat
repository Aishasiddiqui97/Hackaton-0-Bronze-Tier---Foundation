@echo off
echo ========================================
echo Installing Playwright Automation
echo ========================================
echo.
echo This will install:
echo - Playwright (better than Selenium)
echo - Browser drivers
echo - Required dependencies
echo.
pause

echo.
echo [1/3] Installing Playwright...
pip install playwright

echo.
echo [2/3] Installing browser drivers...
python -m playwright install chromium

echo.
echo [3/3] Installing additional dependencies...
pip install python-dotenv watchdog

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next: Run autonomous_poster.py
echo.
pause
