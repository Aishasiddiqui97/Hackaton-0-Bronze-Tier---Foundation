@echo off
echo ========================================
echo Quick LinkedIn Post (5 seconds)
echo ========================================
echo.
echo This will:
echo 1. Copy post content to clipboard
echo 2. Open LinkedIn in browser
echo 3. You just paste and click Post!
echo.
pause

python prepare_linkedin_post.py

echo.
echo ========================================
echo Ready to Post!
echo ========================================
echo.
echo On LinkedIn:
echo 1. Click "Start a post"
echo 2. Press Ctrl+V (paste)
echo 3. Click "Post"
echo.
echo Done in 5 seconds! ✅
echo.
pause
