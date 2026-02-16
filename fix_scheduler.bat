@echo off
REM Fix the Task Scheduler configuration

echo Removing old task...
schtasks /delete /tn "Digital FTE Auto Start" /f

echo.
echo Creating new task with correct path...
schtasks /create /tn "Digital FTE Auto Start" /tr "E:\Python.py\Hackaton 0\start_all_watchers.bat" /sc onstart /rl highest /f

echo.
echo Task recreated successfully!
echo.
echo Testing the task now...
schtasks /run /tn "Digital FTE Auto Start"

echo.
echo Check if 4 command windows opened (Vault, Gmail, LinkedIn, WhatsApp watchers)
echo.
pause
