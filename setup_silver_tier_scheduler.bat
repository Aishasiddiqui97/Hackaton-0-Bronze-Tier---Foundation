@echo off
REM Silver Tier - Windows Task Scheduler Setup
REM This creates the automated scheduling for your Silver Tier system

echo ========================================
echo   SILVER TIER SCHEDULER SETUP
echo ========================================
echo.

echo Creating Windows Task Scheduler entries...
echo.

REM Create the main Gold Tier autonomous task
schtasks /create /tn "Silver_Tier_Autonomous_System" /tr "python \"%~dp0gold_tier_autonomous.py\"" /sc minute /mo 15 /ru "SYSTEM" /f
if %errorlevel% equ 0 (
    echo [SUCCESS] Main autonomous system scheduled every 15 minutes
) else (
    echo [ERROR] Failed to create main task
)

REM Create the watcher system task
schtasks /create /tn "Silver_Tier_Vault_Watcher" /tr "python \"%~dp0AI_Employee_Vault\watcher.py\"" /sc onstart /ru "SYSTEM" /f
if %errorlevel% equ 0 (
    echo [SUCCESS] Vault watcher scheduled to start on boot
) else (
    echo [ERROR] Failed to create watcher task
)

REM Create weekly CEO briefing task (Monday 8 AM)
schtasks /create /tn "Silver_Tier_CEO_Briefing" /tr "python \"%~dp0AI_Employee_Vault\scripts\ceo_briefing.py\"" /sc weekly /d MON /st 08:00 /ru "SYSTEM" /f
if %errorlevel% equ 0 (
    echo [SUCCESS] CEO briefing scheduled for Monday 8 AM
) else (
    echo [ERROR] Failed to create CEO briefing task
)

REM Create daily Odoo sync task (9 AM daily)
schtasks /create /tn "Silver_Tier_Odoo_Sync" /tr "python \"%~dp0odoo_daily_sync.py\"" /sc daily /st 09:00 /ru "SYSTEM" /f
if %errorlevel% equ 0 (
    echo [SUCCESS] Odoo sync scheduled daily at 9 AM
) else (
    echo [ERROR] Failed to create Odoo sync task
)

echo.
echo ========================================
echo   SCHEDULER SETUP COMPLETE
echo ========================================
echo.
echo Your Silver Tier system is now scheduled:
echo.
echo - Main System: Every 15 minutes
echo - Vault Watcher: Starts on boot
echo - CEO Briefing: Monday 8 AM
echo - Odoo Sync: Daily 9 AM
echo.
echo To verify tasks:
echo   schtasks /query /tn "Silver_Tier*"
echo.
echo To start immediately:
echo   schtasks /run /tn "Silver_Tier_Autonomous_System"
echo.
pause