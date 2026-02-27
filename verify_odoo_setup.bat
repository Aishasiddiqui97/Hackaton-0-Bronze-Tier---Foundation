@echo off
echo ========================================
echo Odoo Setup Verification
echo ========================================
echo.

echo [1/5] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker not found. Please install Docker Desktop.
    goto :end
)
echo [OK] Docker is installed
echo.

echo [2/5] Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker Compose not found.
    goto :end
)
echo [OK] Docker Compose is installed
echo.

echo [3/5] Checking required files...
if not exist "docker-compose.yml" (
    echo [X] docker-compose.yml not found
    goto :end
)
echo [OK] docker-compose.yml exists

if not exist "config\odoo.conf" (
    echo [X] config\odoo.conf not found
    goto :end
)
echo [OK] config\odoo.conf exists

if not exist ".env" (
    echo [!] Warning: .env file not found
    echo     Using default configuration
) else (
    echo [OK] .env file exists
)
echo.

echo [4/5] Checking container status...
docker-compose ps 2>nul | findstr "odoo_app" >nul
if %errorlevel% equ 0 (
    echo [OK] Odoo container exists
    docker-compose ps | findstr "Up"
    if %errorlevel% equ 0 (
        echo [OK] Containers are running
    ) else (
        echo [!] Containers exist but not running
        echo     Run: start_odoo.bat
    )
) else (
    echo [!] Containers not created yet
    echo     Run: start_odoo.bat
)
echo.

echo [5/5] Checking Python dependencies...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found
    goto :end
)
echo [OK] Python is installed

python -c "import dotenv" 2>nul
if %errorlevel% neq 0 (
    echo [!] python-dotenv not installed
    echo     Run: pip install python-dotenv
) else (
    echo [OK] python-dotenv is installed
)
echo.

echo ========================================
echo Verification Summary
echo ========================================
echo.
echo Next steps:
echo 1. Start Odoo: start_odoo.bat
echo 2. Wait 2-3 minutes for initialization
echo 3. Access: http://localhost:8069
echo 4. Test API: python odoo_test_api.py
echo 5. Run demo: python odoo_integration_example.py
echo.
echo Documentation:
echo - Quick Start: ODOO_QUICK_START.md
echo - Full Guide: ODOO_SETUP.md
echo - Main README: ODOO_README.md
echo.

:end
pause
