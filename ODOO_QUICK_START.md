# Odoo Quick Start - 5 Minutes to Running

## 🚀 Start Odoo (Windows)

```bash
# Option 1: Use batch file
start_odoo.bat

# Option 2: Manual command
docker-compose up -d
```

## ⏱️ Wait 2-3 minutes for initialization

Check logs:
```bash
docker-compose logs -f odoo
```

Wait for: `HTTP service (werkzeug) running on 0.0.0.0:8069`

## ✅ Verify

1. **Web UI**: http://localhost:8069
   - Username: `admin`
   - Password: `secure_admin_password`

2. **API Test**:
   ```bash
   pip install python-dotenv
   python odoo_test_api.py
   ```

## 🔌 Use in Python

```python
from odoo_integration_example import OdooClient

client = OdooClient()
client.authenticate()

# Get accounting summary
summary = client.get_accounting_summary()
print(summary)

# Search customers
customers = client.search_customers(name="John")

# Get unpaid invoices
unpaid = client.get_unpaid_invoices()
```

## 🛑 Stop Odoo

```bash
# Option 1: Use batch file
stop_odoo.bat

# Option 2: Manual command
docker-compose down
```

## 📊 Common Commands

```bash
# View logs
docker-compose logs -f odoo

# Restart
docker-compose restart odoo

# Check status
docker-compose ps

# Remove everything (CAUTION: deletes data)
docker-compose down -v
```

## 🔧 Troubleshooting

**Port 8069 already in use?**
```bash
# Find what's using the port
netstat -ano | findstr :8069

# Kill the process or change port in docker-compose.yml
```

**Can't connect to API?**
```bash
# Check containers are running
docker-compose ps

# Both should show "Up" status
```

**Authentication failed?**
- Verify credentials in `.env` match `config/odoo.conf`
- Default password: `secure_admin_password`

## 📚 Full Documentation

See `ODOO_SETUP.md` for complete guide.

---

**That's it!** Your Odoo instance is ready for AI Employee integration.
