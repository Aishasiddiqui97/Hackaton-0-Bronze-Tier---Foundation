@echo off
echo ========================================
echo Post to LinkedIn - Direct
echo ========================================
echo.

echo Available posts:
dir /b "03_Posted\History\*.md"
echo.

set /p filename="Enter filename to post: "

if "%filename%"=="" (
    echo ❌ No filename provided
    pause
    exit /b 1
)

echo.
echo Posting: %filename%
python linkedin_auto_poster.py "03_Posted\History\%filename%"

pause
