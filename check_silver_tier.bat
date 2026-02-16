@echo off
REM Quick verification script
echo Checking if Task Scheduler is configured...
echo.

schtasks /query /fo LIST /v | findstr /i "Digital FTE" >nul 2>&1

if %errorlevel% equ 0 (
    echo [SUCCESS] Task Scheduler is configured!
    echo Silver Tier is COMPLETE!
) else (
    echo [PENDING] Task Scheduler NOT configured yet.
    echo Silver Tier is 95%% complete.
    echo.
    echo Follow SCHEDULER_SETUP.md to complete the final step.
)

echo.
pause
