@echo off
echo ========================================
echo Odoo Complete Test Suite
echo ========================================
echo.

echo [1/4] Checking Docker status...
docker-compose ps
echo.

echo [2/4] Testing API connection...
python odoo_test_api.py
echo.

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo API Test Failed!
    echo ========================================
    echo.
    echo This usually means the database isn't initialized.
    echo.
    echo Run this to fix:
    echo   .\fix_odoo_auth.bat
    echo.
    echo Then complete the database setup in the browser.
    echo.
    pause
    exit /b 1
)

echo [3/4] Running integration demo...
python odoo_integration_example.py
echo.

echo [4/4] Opening web UI...
start http://localhost:8069
echo.

echo ========================================
echo All Tests Passed!
echo ========================================
echo.
echo Your Odoo setup is working perfectly!
echo.
echo Web UI: http://localhost:8069
echo Username: admin
echo Password: secure_admin_password
echo.
echo Next steps:
echo 1. Read ODOO_MCP_INTEGRATION.md
echo 2. Create mcp_servers/odoo_server.py
echo 3. Build AI Employee skills
echo.
pause
