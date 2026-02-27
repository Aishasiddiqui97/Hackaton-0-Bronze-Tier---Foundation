@echo off
echo ========================================
echo Social Media Post Status
echo ========================================
echo.

echo [LinkedIn Posts]
echo Posted:
dir "03_Posted\History\POSTED_LinkedIn*.md" /B 2>nul | find /C /V ""
echo Pending:
dir "03_Posted\History\LinkedIn*.md" /B 2>nul | findstr /V "POSTED_" | find /C /V ""
echo.

echo [Twitter Posts]
echo Posted:
dir "03_Posted\History\POSTED_Twitter*.md" /B 2>nul | find /C /V ""
echo Pending:
dir "03_Posted\History\Twitter*.md" /B 2>nul | findstr /V "POSTED_" | find /C /V ""
echo.

echo [Facebook Posts]
echo Posted:
dir "03_Posted\History\POSTED_Facebook*.md" /B 2>nul | find /C /V ""
echo Pending:
dir "03_Posted\History\Facebook*.md" /B 2>nul | findstr /V "POSTED_" | find /C /V ""
echo.

echo [Instagram Posts]
echo Posted:
dir "03_Posted\History\POSTED_Instagram*.md" /B 2>nul | find /C /V ""
echo Pending:
dir "03_Posted\History\Instagram*.md" /B 2>nul | findstr /V "POSTED_" | find /C /V ""
echo.

echo ========================================
echo Detailed List
echo ========================================
echo.

echo POSTED (Already Published):
dir "03_Posted\History\POSTED_*.md" /B 2>nul
echo.

echo PENDING (Need to Post):
dir "03_Posted\History" /B 2>nul | findstr /V "POSTED_"
echo.

pause
