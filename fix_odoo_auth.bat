@echo off
echo ========================================
echo Odoo Authentication Fix
echo ========================================
echo.

echo Checking current status...
docker-compose ps

echo.
echo This will fix authentication issues by:
echo 1. Stopping containers
echo 2. Removing old database
echo 3. Starting fresh
echo.
echo WARNING: This will delete all existing data!
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [Step 1/5] Stopping containers...
docker-compose down

echo.
echo [Step 2/5] Removing volumes (database)...
docker-compose down -v

echo.
echo [Step 3/5] Starting containers...
docker-compose up -d

echo.
echo [Step 4/5] Waiting for startup (90 seconds)...
echo You can watch logs in another terminal with:
echo docker-compose logs -f odoo
timeout /t 90 /nobreak >nul

echo.
echo [Step 5/5] Opening browser for database setup...
start http://localhost:8069

echo.
echo ========================================
echo Database Setup Instructions
echo ========================================
echo.
echo You should see "Create a new database" page
echo.
echo Fill in:
echo   Master Password: secure_admin_password
echo   Database Name: odoo
echo   Email: admin@example.com  
echo   Password: secure_admin_password
echo   Language: English
echo   Country: (select your country)
echo.
echo Click "Create Database" and wait 2-3 minutes
echo.
echo After setup completes, test with:
echo   python odoo_test_api.py
echo.
echo If you don't see the setup page, wait another minute
echo and refresh the browser.
echo.
pause
