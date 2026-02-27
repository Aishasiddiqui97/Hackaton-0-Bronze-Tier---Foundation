# Odoo Docker Setup Guide

Complete guide for running Odoo in Docker for your Personal AI Employee system.

## 📁 Folder Structure

```
your-project/
├── docker-compose.yml          # Main Docker configuration
├── config/
│   └── odoo.conf              # Odoo configuration file
├── addons/                    # Custom Odoo modules (optional)
│   └── .gitkeep
├── odoo_test_api.py           # API test script
├── .env                       # Environment variables
└── ODOO_SETUP.md             # This file
```

## 🚀 Quick Start

### 1. Start Odoo

```bash
# Start all containers
docker-compose up -d

# Check container status
docker-compose ps

# View logs
docker-compose logs -f odoo
```

**First startup takes 2-3 minutes** as Odoo initializes the database.

### 2. Verify Installation

Wait for this log message:
```
odoo_app | odoo.service.server: HTTP service (werkzeug) running on 0.0.0.0:8069
```

Then access:
- Web UI: http://localhost:8069
- Default credentials:
  - Email: `admin`
  - Password: `secure_admin_password`
  - Database: `odoo` (auto-selected)

### 3. Test API Connection

```bash
# Install Python dependencies
pip install python-dotenv

# Run API test
python odoo_test_api.py
```

Expected output:
```
✓ Connected to Odoo 17.0
✓ Authentication successful
✓ ALL TESTS PASSED - Odoo API is ready!
```

## 🔧 Configuration Details

### Environment Variables (.env)

Your existing `.env` configuration is correct:
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=secure_admin_password
```

### Docker Compose Features

- **Auto-initialization**: Database created automatically on first run
- **Health checks**: Ensures PostgreSQL is ready before Odoo starts
- **Persistent data**: Volumes preserve data across restarts
- **Auto-restart**: Containers restart automatically on failure
- **Network isolation**: Dedicated network for Odoo services

### Ports

- `8069`: Odoo web interface and XML-RPC API
- PostgreSQL runs internally (not exposed)

## 🔌 Python Integration Example

```python
import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
url = os.getenv('ODOO_URL')
db = os.getenv('ODOO_DB')
username = os.getenv('ODOO_USERNAME')
password = os.getenv('ODOO_PASSWORD')

# Authenticate
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Access models
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Example: Create a customer
partner_id = models.execute_kw(
    db, uid, password,
    'res.partner', 'create',
    [{'name': 'AI Employee', 'email': 'ai@company.com'}]
)

# Example: Search invoices
invoices = models.execute_kw(
    db, uid, password,
    'account.move', 'search_read',
    [[('move_type', '=', 'out_invoice')]],
    {'fields': ['name', 'partner_id', 'amount_total'], 'limit': 10}
)
```

## 📊 Common Operations

### Start/Stop

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Stop and remove volumes (CAUTION: deletes all data)
docker-compose down -v
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View Odoo logs only
docker-compose logs -f odoo

# View PostgreSQL logs
docker-compose logs -f postgres

# Enter Odoo container
docker exec -it odoo_app bash

# Enter PostgreSQL container
docker exec -it odoo_postgres psql -U odoo -d odoo
```

### Restart After Changes

```bash
# Restart Odoo only
docker-compose restart odoo

# Rebuild after config changes
docker-compose up -d --force-recreate
```

## 🔐 Security Notes

### For Development
Current setup is optimized for local development with:
- Simple passwords
- All interfaces exposed
- Database management enabled

### For Production
Update these settings in `config/odoo.conf`:
```ini
# Use strong passwords
admin_passwd = <generate-strong-password>

# Restrict interfaces
http_interface = 127.0.0.1
xmlrpc_interface = 127.0.0.1

# Disable database management UI
list_db = False

# Use environment-specific database filter
dbfilter = ^production_db$
```

## 🎯 Key Odoo Models for AI Employee

### Accounting & Finance
- `account.move`: Invoices and bills
- `account.payment`: Payments
- `account.journal`: Journals
- `account.account`: Chart of accounts

### Contacts & CRM
- `res.partner`: Customers, vendors, contacts
- `crm.lead`: Leads and opportunities
- `sale.order`: Sales orders

### Inventory & Products
- `product.product`: Products
- `stock.picking`: Deliveries and receipts
- `purchase.order`: Purchase orders

### HR & Employees
- `hr.employee`: Employees
- `hr.attendance`: Attendance records
- `hr.leave`: Time off requests

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs odoo

# Common issue: Port already in use
# Solution: Stop other services on port 8069 or change port in docker-compose.yml
```

### Database connection failed
```bash
# Ensure PostgreSQL is healthy
docker-compose ps

# Should show "healthy" status for postgres
# If not, restart:
docker-compose restart postgres
```

### Authentication failed
```bash
# Reset admin password
docker exec -it odoo_app odoo shell -d odoo
# In Odoo shell:
# env['res.users'].browse(2).write({'password': 'secure_admin_password'})
```

### API returns empty results
- Ensure you're authenticated with correct credentials
- Check user has proper access rights in Odoo UI
- Verify model names are correct (case-sensitive)

## 📈 Performance Optimization

### For Hackathon/Demo
Current settings are optimized for quick startup and demos.

### For Production
Update `config/odoo.conf`:
```ini
# Increase workers for better performance
workers = 4

# Add limits
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200
```

## 🔄 Backup & Restore

### Backup
```bash
# Backup database
docker exec odoo_postgres pg_dump -U odoo odoo > odoo_backup.sql

# Backup filestore
docker cp odoo_app:/var/lib/odoo ./odoo_filestore_backup
```

### Restore
```bash
# Restore database
docker exec -i odoo_postgres psql -U odoo odoo < odoo_backup.sql

# Restore filestore
docker cp ./odoo_filestore_backup odoo_app:/var/lib/odoo
```

## ✅ Verification Checklist

- [ ] Containers running: `docker-compose ps`
- [ ] Web UI accessible: http://localhost:8069
- [ ] Can login with admin credentials
- [ ] API test passes: `python odoo_test_api.py`
- [ ] Can create/read records via XML-RPC
- [ ] Data persists after restart

## 🎓 Next Steps

1. Install required Odoo apps via UI (Accounting, CRM, etc.)
2. Configure company information
3. Set up chart of accounts
4. Create API integration in your Python backend
5. Build MCP server for Odoo integration

## 📚 Resources

- [Odoo Documentation](https://www.odoo.com/documentation/17.0/)
- [XML-RPC API Guide](https://www.odoo.com/documentation/17.0/developer/reference/external_api.html)
- [Odoo Docker Hub](https://hub.docker.com/_/odoo)

---

**Ready for integration!** Your Odoo instance is configured for XML-RPC API access and ready to connect with your Personal AI Employee system.
