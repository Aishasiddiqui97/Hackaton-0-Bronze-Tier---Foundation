@echo off
echo ========================================
echo Odoo Database Reset
echo ========================================
echo.
echo This will DELETE the existing 'odoo' database
echo and let you create a fresh one.
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/5] Stopping Odoo container...
docker-compose stop odoo

echo.
echo [2/5] Deleting 'odoo' database...
docker exec -it odoo_postgres psql -U odoo -d postgres -c "DROP DATABASE IF EXISTS odoo;"

echo.
echo [3/5] Restarting containers...
docker-compose up -d

echo.
echo [4/5] Waiting for startup (60 seconds)...
timeout /t 60 /nobreak >nul

echo.
echo [5/5] Opening browser...
start http://localhost:8069

echo.
echo ========================================
echo Database Reset Complete!
echo ========================================
echo.
echo Now in the browser:
echo.
echo 1. Fill in the "Create a new database" form:
echo    Master Password: secure_admin_password
echo    Database Name: odoo
echo    Email: admin@example.com
echo    Password: secure_admin_password
echo.
echo 2. Click "Create Database"
echo.
echo 3. Wait 2-3 minutes
echo.
echo 4. Test with: python odoo_test_api.py
echo.
pause
