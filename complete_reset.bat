@echo off
echo ========================================
echo Complete Odoo Reset (Nuclear Option)
echo ========================================
echo.
echo WARNING: This will DELETE ALL DATA!
echo.
echo This will:
echo 1. Stop all containers
echo 2. Remove all volumes
echo 3. Start completely fresh
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/6] Stopping containers...
docker-compose down

echo.
echo [2/6] Listing volumes...
docker volume ls | findstr odoo

echo.
echo [3/6] Removing odoo-db-data volume...
docker volume rm hackaton0_odoo-db-data 2>nul
if %errorlevel% neq 0 (
    echo Trying with force...
    docker volume rm -f hackaton0_odoo-db-data 2>nul
)

echo.
echo [4/6] Removing odoo-web-data volume...
docker volume rm hackaton0_odoo-web-data 2>nul
if %errorlevel% neq 0 (
    echo Trying with force...
    docker volume rm -f hackaton0_odoo-web-data 2>nul
)

echo.
echo [5/6] Starting fresh containers...
docker-compose up -d

echo.
echo [6/6] Waiting for startup (90 seconds)...
echo Watch logs in another window: docker-compose logs -f odoo
timeout /t 90 /nobreak >nul

echo.
echo Opening browser...
start http://localhost:8069

echo.
echo ========================================
echo Reset Complete!
echo ========================================
echo.
echo Now you should see "Create a new database" page
echo.
echo Fill in:
echo   Master Password: secure_admin_password
echo   Database Name: odoo
echo   Email: admin@example.com
echo   Password: secure_admin_password
echo.
echo If you still see error, wait 1 more minute and refresh
echo.
pause
