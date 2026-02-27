@echo off
echo ========================================
echo Odoo Database Initialization
echo ========================================
echo.

echo This will:
echo 1. Stop existing containers
echo 2. Remove old database
echo 3. Start fresh Odoo instance
echo 4. Initialize database via web UI
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/4] Stopping containers...
docker-compose down -v

echo.
echo [2/4] Starting fresh containers...
docker-compose up -d

echo.
echo [3/4] Waiting for Odoo to start (60 seconds)...
timeout /t 60 /nobreak >nul

echo.
echo [4/4] Opening web browser...
start http://localhost:8069

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. In the browser, you'll see "Create a new database"
echo.
echo 2. Fill in the form:
echo    Master Password: secure_admin_password
echo    Database Name: odoo
echo    Email: admin@example.com
echo    Password: secure_admin_password
echo    Language: English
echo    Country: Your country
echo.
echo 3. Click "Create Database"
echo.
echo 4. Wait 2-3 minutes for initialization
echo.
echo 5. Login with:
echo    Username: admin
echo    Password: secure_admin_password
echo.
echo 6. Then test API:
echo    python odoo_test_api.py
echo.
pause
