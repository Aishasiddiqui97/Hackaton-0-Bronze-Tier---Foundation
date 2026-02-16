@echo off
REM Digital FTE - Start All Watchers
REM Run this script to launch all monitoring services

cd /d "%~dp0"

echo Starting Digital FTE System...
echo ================================

REM Start Vault Watcher (Main Engine)
start "Vault Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\watcher.py"
timeout /t 2 /nobreak >nul

REM Start Gmail Watcher
start "Gmail Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\scripts\gmail_watcher.py"
timeout /t 2 /nobreak >nul

REM Start LinkedIn Watcher
start "LinkedIn Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe scripts\linkedin_watcher.py"
timeout /t 2 /nobreak >nul

REM Start WhatsApp Watcher
start "WhatsApp Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe scripts\whatsapp_watcher.py"

echo.
echo All watchers started successfully!
echo Close this window to keep watchers running.
echo.
pause
