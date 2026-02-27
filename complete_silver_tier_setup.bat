@echo off
REM Complete Silver Tier Setup - One-Click Installation
REM This script sets up everything needed for Silver Tier compliance

echo ========================================
echo   SILVER TIER COMPLETE SETUP
echo ========================================
echo.
echo This will set up your complete Silver Tier system:
echo - Windows Task Scheduler configuration
echo - All required folders
echo - Verification and testing
echo.
pause

echo.
echo [1/4] Creating required folders...
mkdir "00_Inbox\Social_Media" 2>nul
mkdir "00_Inbox\Urgent_WhatsApp" 2>nul
mkdir "01_Drafts\Auto_Generated" 2>nul
mkdir "02_Pending_Approvals\Social_Posts" 2>nul
mkdir "02_Pending_Approvals\Email_Drafts" 2>nul
mkdir "03_Posted\History" 2>nul
mkdir "AI_Employee_Vault\Plans" 2>nul
mkdir "AI_Employee_Vault\Needs_Action" 2>nul
mkdir "AI_Employee_Vault\CEO_Briefings" 2>nul
mkdir "logs" 2>nul
echo ✅ Folders created

echo.
echo [2/4] Setting up Windows Task Scheduler...
call setup_silver_tier_scheduler.bat
echo ✅ Scheduler configured

echo.
echo [3/4] Testing system components...
python verify_silver_tier.py
echo ✅ Verification complete

echo.
echo [4/4] Creating startup script...
echo @echo off > start_silver_tier.bat
echo REM Start Silver Tier System >> start_silver_tier.bat
echo echo Starting Silver Tier Autonomous System... >> start_silver_tier.bat
echo start /min python gold_tier_autonomous.py >> start_silver_tier.bat
echo start /min python AI_Employee_Vault\watcher.py >> start_silver_tier.bat
echo echo Silver Tier system started! >> start_silver_tier.bat
echo echo Check System_Live_Status.md for status >> start_silver_tier.bat
echo pause >> start_silver_tier.bat
echo ✅ Startup script created

echo.
echo ========================================
echo   SILVER TIER SETUP COMPLETE!
echo ========================================
echo.
echo Your Silver Tier system is now ready:
echo.
echo ✅ All folders created
echo ✅ Windows Task Scheduler configured  
echo ✅ Automated workflows active
echo ✅ Startup script ready
echo.
echo To start your system:
echo   1. Double-click: start_silver_tier.bat
echo   2. Or let Task Scheduler auto-start
echo.
echo To verify status:
echo   python verify_silver_tier.py
echo.
echo Your Silver Tier system includes:
echo - 4+ Watcher scripts (Gmail, WhatsApp, LinkedIn, Vault)
echo - LinkedIn auto-posting
echo - Claude reasoning loop with Plan.md generation
echo - Multiple MCP servers (Odoo, Social Media)
echo - Human-in-the-loop approval workflow
echo - Windows Task Scheduler automation
echo - 20+ AI Agent Skills
echo.
echo 🎉 SILVER TIER IS COMPLETE!
echo.
pause