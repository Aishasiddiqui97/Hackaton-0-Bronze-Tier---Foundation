@echo off
echo ========================================
echo Direct Admin Password Reset
echo ========================================
echo.
echo This will reset admin password directly
echo in the PostgreSQL database.
echo.
pause

echo.
echo [1/3] Stopping Odoo to unlock database...
docker-compose stop odoo

echo.
echo [2/3] Resetting admin password in database...
echo.
docker exec -it odoo_postgres psql -U odoo -d odoo -c "UPDATE res_users SET password='secure_admin_password' WHERE login='admin';"

echo.
echo Verifying update...
docker exec -it odoo_postgres psql -U odoo -d odoo -c "SELECT login, password FROM res_users WHERE login='admin';"

echo.
echo [3/3] Starting Odoo...
docker-compose start odoo

echo.
echo Waiting for Odoo to start (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo Testing API...
echo ========================================
python odoo_test_api.py

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Try logging in:
echo   URL: http://localhost:8069
echo   Username: admin
echo   Password: secure_admin_password
echo.
pause
