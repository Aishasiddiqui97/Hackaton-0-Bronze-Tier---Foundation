@echo off
echo ========================================
echo LinkedIn Auto-Poster (Fully Automatic)
echo ========================================
echo.

python linkedin_simple_poster.py "03_Posted\History\POSTED_LinkedIn_Post_20260225_172956.md"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Post created on LinkedIn
    echo ========================================
) else (
    echo.
    echo ========================================
    echo FAILED! Check error screenshots
    echo ========================================
)

echo.
pause
