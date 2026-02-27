@echo off
echo ========================================
echo Check GitHub Connection
echo ========================================
echo.

echo Testing internet connection...
ping google.com -n 1 >nul 2>&1
if errorlevel 1 (
    echo ❌ No internet connection!
    echo Please check your network.
    pause
    exit /b 1
) else (
    echo ✅ Internet connected
)

echo.
echo Testing GitHub connection...
ping github.com -n 1 >nul 2>&1
if errorlevel 1 (
    echo ❌ Cannot reach GitHub!
    echo.
    echo Possible solutions:
    echo 1. Check if GitHub is down: https://www.githubstatus.com/
    echo 2. Try using VPN
    echo 3. Check firewall settings
    echo 4. Try: git config --global http.proxy ""
    pause
    exit /b 1
) else (
    echo ✅ GitHub reachable
)

echo.
echo Testing Git authentication...
git ls-remote https://github.com/Aishasiddiqui97/Hackaton-0.git >nul 2>&1
if errorlevel 1 (
    echo ❌ Authentication failed!
    echo.
    echo Please setup authentication:
    echo 1. GitHub CLI: gh auth login
    echo 2. Or use personal access token
    pause
    exit /b 1
) else (
    echo ✅ Authentication working
)

echo.
echo ========================================
echo ✅ All checks passed!
echo ========================================
echo You can now push to GitHub.
echo.
pause
