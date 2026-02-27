@echo off
echo ========================================
echo Post to LinkedIn (Browser Automation)
echo ========================================
echo.

if "%1"=="" (
    echo Using latest LinkedIn post from 03_Posted\History\
    python linkedin_auto_poster.py
) else (
    echo Posting file: %1
    python linkedin_auto_poster.py "%1"
)

echo.
pause
