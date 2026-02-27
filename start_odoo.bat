@echo off
echo ========================================
echo Starting Odoo Docker Environment
echo ========================================
echo.

echo [1/3] Starting Docker containers...
docker-compose up -d

echo.
echo [2/3] Waiting for Odoo to initialize...
echo This may take 2-3 minutes on first run...
timeout /t 30 /nobreak >nul

echo.
echo [3/3] Checking container status...
docker-compose ps

echo.
echo ========================================
echo Odoo is starting up!
echo ========================================
echo.
echo Web UI: http://localhost:8069
echo Username: admin
echo Password: secure_admin_password
echo Database: odoo
echo.
echo To view logs: docker-compose logs -f odoo
echo To test API: python odoo_test_api.py
echo.
pause
