# Quick Fix Guide

## Issue 1: Running Batch Files in PowerShell

In PowerShell, you need to prefix batch files with `.\`

### Wrong:
```powershell
start_odoo.bat
```

### Correct:
```powershell
.\start_odoo.bat
```

## Issue 2: Authentication Failed

The Odoo database exists but the admin user needs to be initialized properly.

### Solution: Recreate with proper initialization

Run these commands:

```powershell
# 1. Stop and remove everything
docker-compose down -v

# 2. Start fresh
docker-compose up -d

# 3. Wait 3-4 minutes for full initialization
# Watch logs to see when ready:
docker-compose logs -f odoo
```

Look for this message in logs:
```
odoo.service.server: HTTP service (werkzeug) running on 0.0.0.0:8069
```

Then press Ctrl+C to exit logs.

### Alternative: Initialize via Web UI

1. Go to http://localhost:8069
2. You'll see database creation screen
3. Fill in:
   - Master Password: `secure_admin_password`
   - Database Name: `odoo`
   - Email: `admin@example.com`
   - Password: `secure_admin_password`
   - Phone: (optional)
   - Language: English
   - Country: Your country
4. Click "Create Database"
5. Wait 2-3 minutes
6. Login with: admin / secure_admin_password

Then test API again:
```powershell
python odoo_test_api.py
```
