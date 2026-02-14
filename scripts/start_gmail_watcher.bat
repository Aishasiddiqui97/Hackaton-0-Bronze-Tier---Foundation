@echo off
REM Gmail Watcher Service Launcher
REM This script runs the Gmail Watcher with proper error handling

cd /d "%~dp0.."
echo Starting Gmail Watcher Service...
echo Working Directory: %CD%
echo.

REM Activate virtual environment and run watcher
AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\scripts\gmail_watcher.py

REM If the script exits, log it and restart after delay
echo.
echo Gmail Watcher stopped unexpectedly at %date% %time%
echo Waiting 30 seconds before restart...
timeout /t 30 /nobreak
goto :eof
