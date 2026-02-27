@echo off
echo ========================================
echo Quick Post to All Platforms
echo ========================================
echo.

echo Checking for posts to publish...
echo.

set /a count=0

echo Twitter Posts:
for %%f in ("03_Posted\History\Twitter_Post_*.md") do (
    if not "%%~nxf"=="Twitter_Post_*.md" (
        echo   - %%~nxf
        set /a count+=1
    )
)

echo.
echo Facebook Posts:
for %%f in ("03_Posted\History\Facebook_Post_*.md") do (
    if not "%%~nxf"=="Facebook_Post_*.md" (
        echo   - %%~nxf
        set /a count+=1
    )
)

echo.
echo Instagram Posts:
for %%f in ("03_Posted\History\Instagram_Post_*.md") do (
    if not "%%~nxf"=="Instagram_Post_*.md" (
        echo   - %%~nxf
        set /a count+=1
    )
)

echo.
if %count%==0 (
    echo No posts found to publish.
    echo.
    echo Generate new posts with: generate_all_posts.bat
    pause
    exit /b
)

echo ========================================
echo Manual Posting Guide
echo ========================================
echo.
echo I'll copy each post to clipboard and
echo open the platform. You just:
echo 1. Paste (Ctrl+V)
echo 2. Click Post
echo 3. Takes 10 seconds each!
echo.
pause

echo.
echo [1/3] Twitter Posts...
for %%f in ("03_Posted\History\Twitter_Post_*.md") do (
    if not "%%~nxf"=="Twitter_Post_*.md" (
        echo.
        echo Processing: %%~nxf
        python prepare_linkedin_post.py "%%f"
        echo.
        echo Opening Twitter...
        start https://twitter.com/compose/tweet
        echo.
        echo Paste content and click Post!
        pause
        
        echo Marking as posted...
        ren "%%f" "POSTED_%%~nxf"
    )
)

echo.
echo [2/3] Facebook Posts...
for %%f in ("03_Posted\History\Facebook_Post_*.md") do (
    if not "%%~nxf"=="Facebook_Post_*.md" (
        echo.
        echo Processing: %%~nxf
        python prepare_linkedin_post.py "%%f"
        echo.
        echo Opening Facebook...
        start https://www.facebook.com/
        echo.
        echo Paste content and click Post!
        pause
        
        echo Marking as posted...
        ren "%%f" "POSTED_%%~nxf"
    )
)

echo.
echo [3/3] Instagram Posts...
for %%f in ("03_Posted\History\Instagram_Post_*.md") do (
    if not "%%~nxf"=="Instagram_Post_*.md" (
        echo.
        echo Processing: %%~nxf
        python prepare_linkedin_post.py "%%f"
        echo.
        echo Opening Instagram...
        start https://www.instagram.com/
        echo.
        echo Paste caption and upload image!
        pause
        
        echo Marking as posted...
        ren "%%f" "POSTED_%%~nxf"
    )
)

echo.
echo ========================================
echo All Posts Published!
echo ========================================
echo.
echo Great job! All platforms updated.
echo.
pause
