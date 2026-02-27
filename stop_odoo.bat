@echo off
echo ========================================
echo Stopping Odoo Docker Environment
echo ========================================
echo.

docker-compose down

echo.
echo Odoo containers stopped.
echo Data is preserved in Docker volumes.
echo.
echo To start again: start_odoo.bat
echo To remove all data: docker-compose down -v
echo.
pause
