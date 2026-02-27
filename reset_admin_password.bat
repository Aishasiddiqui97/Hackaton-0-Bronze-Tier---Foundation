@echo off
echo ========================================
echo Reset Admin Password (Use Existing DB)
echo ========================================
echo.
echo This will reset the admin password in the
echo existing 'odoo' database.
echo.
echo No data will be lost!
echo.
pause

echo.
echo [1/2] Accessing Odoo shell...
echo.
echo Running command to reset password...
echo Please wait...
echo.

docker exec -it odoo_app odoo shell -d odoo --no-http -c "env['res.users'].browse(2).write({'password': 'secure_admin_password'}); env.cr.commit()"

echo.
echo [2/2] Testing API...
python odoo_test_api.py

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo If authentication still fails, the database
echo might be corrupted. Run:
echo   .\complete_reset.bat
echo.
pause
