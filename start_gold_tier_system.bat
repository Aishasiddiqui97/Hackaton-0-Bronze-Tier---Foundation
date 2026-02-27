@echo off
echo ========================================
echo GOLD TIER AUTONOMOUS SYSTEM
echo ========================================
echo.
echo This will start the complete autonomous system:
echo.
echo - LinkedIn: Auto-posting
echo - Twitter: Auto-posting (if API configured)
echo - Facebook: Auto-posting (if token valid)
echo - Odoo: Dashboard updates (Monday 8 AM)
echo - Auto-generate posts every 12 hours
echo - Check folders every 15 minutes
echo.
echo Ralph Wiggum Loop Mode: ACTIVE
echo (Never stops, never asks)
echo.
pause

echo.
echo Starting Gold Tier System...
python gold_tier_autonomous.py

pause
