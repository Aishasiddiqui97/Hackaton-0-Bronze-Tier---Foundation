@echo off 
REM Start Silver Tier System 
echo Starting Silver Tier Autonomous System... 
start /min python gold_tier_autonomous.py 
start /min python AI_Employee_Vault\watcher.py 
echo Silver Tier system started! 
echo Check System_Live_Status.md for status 
pause 
