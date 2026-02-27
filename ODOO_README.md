# 🏢 Odoo Integration for Personal AI Employee

Complete Dockerized Odoo setup with XML-RPC API access for automated accounting and business management.

## 📦 What's Included

```
odoo-setup/
├── docker-compose.yml              # Docker orchestration
├── config/
│   └── odoo.conf                  # Odoo configuration
├── addons/                        # Custom modules directory
├── start_odoo.bat                 # Windows start script
├── stop_odoo.bat                  # Windows stop script
├── odoo_test_api.py              # API connection test
├── odoo_integration_example.py    # Integration examples
├── ODOO_SETUP.md                 # Complete documentation
├── ODOO_QUICK_START.md           # 5-minute quick start
└── .env                          # Your existing config
```

## ⚡ Quick Start

### 1. Start Odoo
```bash
start_odoo.bat
```

### 2. Access Web UI
- URL: http://localhost:8069
- Username: `admin`
- Password: `secure_admin_password`
- Database: `odoo` (auto-created)

### 3. Test API
```bash
pip install python-dotenv
python odoo_test_api.py
```

### 4. Run Demo
```bash
python odoo_integration_example.py
```

## 🎯 Key Features

✅ **Fully Automated Setup**
- Auto-creates database
- Pre-configured for API access
- No manual UI configuration needed

✅ **Production-Ready Architecture**
- PostgreSQL database with health checks
- Persistent data volumes
- Auto-restart on failure
- Proper network isolation

✅ **XML-RPC API Enabled**
- Ready for Python integration
- Complete authentication flow
- Example operations included

✅ **Hackathon Optimized**
- Fast startup (2-3 minutes)
- Clean configuration
- Easy to demo

## 🔌 Integration with AI Employee

### Basic Usage

```python
from odoo_integration_example import OdooClient

# Initialize
client = OdooClient()
client.authenticate()

# Get accounting summary
summary = client.get_accounting_summary()
print(f"Total customers: {summary['customers']['total']}")
print(f"Unpaid invoices: {summary['invoices']['unpaid_count']}")
print(f"Unpaid amount: ${summary['invoices']['unpaid_amount']}")

# Search customers
customers = client.search_customers(name="John Doe")

# Get unpaid invoices
unpaid = client.get_unpaid_invoices(limit=10)
for invoice in unpaid:
    print(f"{invoice['name']}: ${invoice['amount_residual']}")
```

### MCP Server Integration

Create `mcp_servers/odoo_server.py`:

```python
from odoo_integration_example import OdooClient

class OdooMCPServer:
    def __init__(self):
        self.client = OdooClient()
        self.client.authenticate()
    
    def get_accounting_summary(self):
        """Get accounting summary for CEO briefing"""
        return self.client.get_accounting_summary()
    
    def get_unpaid_invoices(self):
        """Get list of unpaid invoices for follow-up"""
        return self.client.get_unpaid_invoices()
    
    def search_customer(self, name):
        """Search for customer by name"""
        return self.client.search_customers(name=name)
```

## 📊 Available Operations

### Customer Management
- Create customers/partners
- Search customers
- Update customer information
- Get customer details

### Invoice Management
- Get all invoices
- Filter by state (draft, posted, paid)
- Get unpaid invoices
- Get overdue invoices
- Calculate totals

### Payment Tracking
- Get payment records
- Filter by customer
- Track payment status

### Product Management
- Search products
- Get product details
- Check inventory levels

### Reporting
- Accounting summary
- Customer statistics
- Invoice analytics
- Payment tracking

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Personal AI Employee System         │
│  ┌───────────────────────────────────┐  │
│  │   Python Backend / MCP Server     │  │
│  │   (odoo_integration_example.py)   │  │
│  └───────────────┬───────────────────┘  │
│                  │ XML-RPC                │
│                  │ (port 8069)            │
│  ┌───────────────▼───────────────────┐  │
│  │      Odoo Container               │  │
│  │   - Web UI                        │  │
│  │   - XML-RPC API                   │  │
│  │   - Business Logic                │  │
│  └───────────────┬───────────────────┘  │
│                  │                        │
│  ┌───────────────▼───────────────────┐  │
│  │   PostgreSQL Container            │  │
│  │   - Database: odoo                │  │
│  │   - Persistent Storage            │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## 🔐 Configuration

### Environment Variables (.env)
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=secure_admin_password
```

### Docker Compose
- Odoo: Latest stable (v17.0)
- PostgreSQL: v15
- Volumes: Persistent data storage
- Network: Isolated bridge network

### Odoo Config (config/odoo.conf)
- XML-RPC enabled
- Admin password set
- Database auto-created
- Workers configured
- Logging enabled

## 🛠️ Management Commands

### Start/Stop
```bash
# Start
start_odoo.bat
# or
docker-compose up -d

# Stop
stop_odoo.bat
# or
docker-compose down
```

### Monitoring
```bash
# View logs
docker-compose logs -f odoo

# Check status
docker-compose ps

# Enter container
docker exec -it odoo_app bash
```

### Maintenance
```bash
# Restart
docker-compose restart odoo

# Rebuild
docker-compose up -d --force-recreate

# Backup database
docker exec odoo_postgres pg_dump -U odoo odoo > backup.sql

# Restore database
docker exec -i odoo_postgres psql -U odoo odoo < backup.sql
```

## 🎓 Next Steps

1. **Install Odoo Apps**
   - Go to http://localhost:8069
   - Apps menu → Install:
     - Accounting
     - CRM
     - Sales
     - Inventory (if needed)

2. **Configure Company**
   - Settings → General Settings
   - Set company name, address, logo
   - Configure fiscal year

3. **Set Up Chart of Accounts**
   - Accounting → Configuration
   - Choose your country's chart of accounts

4. **Create MCP Server**
   - Use `odoo_integration_example.py` as base
   - Add to your MCP server collection
   - Integrate with AI Employee workflows

5. **Build Automation**
   - Invoice reminders
   - Payment tracking
   - Customer follow-ups
   - Financial reporting

## 📚 Resources

- **Quick Start**: `ODOO_QUICK_START.md`
- **Full Guide**: `ODOO_SETUP.md`
- **API Test**: `python odoo_test_api.py`
- **Demo**: `python odoo_integration_example.py`

### External Links
- [Odoo Documentation](https://www.odoo.com/documentation/17.0/)
- [XML-RPC API Reference](https://www.odoo.com/documentation/17.0/developer/reference/external_api.html)
- [Odoo Docker Image](https://hub.docker.com/_/odoo)

## 🐛 Troubleshooting

### Common Issues

**Port 8069 in use**
```bash
netstat -ano | findstr :8069
# Kill process or change port in docker-compose.yml
```

**Database connection failed**
```bash
docker-compose restart postgres
docker-compose logs postgres
```

**Authentication failed**
- Check credentials in `.env`
- Verify `config/odoo.conf` admin password
- Try resetting password via Odoo shell

**API returns empty results**
- Ensure user has access rights
- Check model names (case-sensitive)
- Verify data exists in Odoo UI

### Getting Help

1. Check logs: `docker-compose logs -f`
2. Review `ODOO_SETUP.md` troubleshooting section
3. Test API: `python odoo_test_api.py`
4. Verify containers: `docker-compose ps`

## ✅ Verification Checklist

- [ ] Docker and Docker Compose installed
- [ ] Containers running: `docker-compose ps`
- [ ] Web UI accessible: http://localhost:8069
- [ ] Can login with admin credentials
- [ ] API test passes: `python odoo_test_api.py`
- [ ] Demo runs successfully: `python odoo_integration_example.py`
- [ ] Data persists after restart
- [ ] Ready for MCP integration

## 🎉 Success!

Your Odoo instance is now:
- ✅ Running in Docker
- ✅ Accessible at http://localhost:8069
- ✅ API-enabled for XML-RPC
- ✅ Ready for AI Employee integration
- ✅ Production-ready architecture
- ✅ Optimized for hackathon demos

**Start building your AI-powered accounting automation!**
