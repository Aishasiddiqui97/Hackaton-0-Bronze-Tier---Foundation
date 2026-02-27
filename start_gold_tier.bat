@echo off
REM Digital FTE - Gold Tier Startup Script
REM Starts all watchers + CEO Briefing scheduler

cd /d "%~dp0"

echo ========================================
echo   Digital FTE - Gold Tier System
echo ========================================
echo.
echo Starting all components...
echo.

REM Start Bronze/Silver Tier Watchers
start "Vault Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\watcher.py"
timeout /t 2 /nobreak >nul

start "Gmail Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\scripts\gmail_watcher.py"
timeout /t 2 /nobreak >nul

start "LinkedIn Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe scripts\linkedin_watcher.py"
timeout /t 2 /nobreak >nul

start "WhatsApp Watcher" cmd /k "AI_Employee_Vault\venv\Scripts\python.exe scripts\whatsapp_watcher.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   All Gold Tier Components Started
echo ========================================
echo.
echo Running Services:
echo   - Vault Watcher (Core Engine)
echo   - Gmail Watcher
echo   - LinkedIn Watcher
echo   - WhatsApp Watcher
echo.
echo MCP Servers (via Claude Desktop):
echo   - Odoo Accounting Server
echo   - Facebook Server
echo   - Instagram Server
echo   - Twitter Server
echo   - Email Server
echo   - LinkedIn Server
echo   - WhatsApp Server
echo   - Vault Watcher Server
echo   - Gmail Server
echo.
echo CEO Briefing:
echo   - Run manually: python scripts\ceo_briefing_generator.py
echo   - Or schedule weekly via Task Scheduler
echo.
echo Close this window to keep all services running.
echo.
pause
