# Odoo MCP Server Integration Guide

How to integrate Odoo with your Personal AI Employee MCP architecture.

## 🎯 Overview

This guide shows how to create an MCP server that connects your AI Employee to Odoo for automated accounting and business management.

## 📁 File Structure

```
mcp_servers/
└── odoo_server.py          # Your Odoo MCP server

# Shared utilities
odoo_integration_example.py  # OdooClient class (reusable)
.env                        # Configuration
```

## 🔧 Step 1: Create Odoo MCP Server

Create `mcp_servers/odoo_server.py`:

```python
#!/usr/bin/env python3
"""
Odoo MCP Server for Personal AI Employee
Provides accounting and business management capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from odoo_integration_example import OdooClient
import json
from datetime import datetime


class OdooMCPServer:
    """MCP Server for Odoo integration"""
    
    def __init__(self):
        self.client = OdooClient()
        self.client.authenticate()
        
    # Tool: Get Accounting Summary
    def get_accounting_summary(self):
        """
        Get comprehensive accounting summary for CEO briefing
        
        Returns:
            dict: Summary with customers, invoices, payments
        """
        return self.client.get_accounting_summary()
    
    # Tool: Get Unpaid Invoices
    def get_unpaid_invoices(self, limit=10):
        """
        Get list of unpaid invoices for follow-up
        
        Args:
            limit (int): Maximum number of invoices to return
            
        Returns:
            list: Unpaid invoices with customer and amount details
        """
        return self.client.get_unpaid_invoices(limit=limit)
    
    # Tool: Search Customer
    def search_customer(self, name, limit=10):
        """
        Search for customers by name
        
        Args:
            name (str): Customer name to search for
            limit (int): Maximum results
            
        Returns:
            list: Matching customers with contact details
        """
        return self.client.search_customers(name=name, limit=limit)
    
    # Tool: Create Customer
    def create_customer(self, name, email=None, phone=None, is_company=False):
        """
        Create a new customer/partner
        
        Args:
            name (str): Customer name
            email (str): Email address
            phone (str): Phone number
            is_company (bool): Whether this is a company
            
        Returns:
            int: New customer ID
        """
        return self.client.create_customer(
            name=name,
            email=email,
            phone=phone,
            is_company=is_company
        )
    
    # Tool: Get Recent Invoices
    def get_recent_invoices(self, limit=10):
        """
        Get recent invoices for monitoring
        
        Args:
            limit (int): Maximum number of invoices
            
        Returns:
            list: Recent invoices with details
        """
        return self.client.get_invoices(limit=limit)
    
    # Tool: Get Customer Invoices
    def get_customer_invoices(self, customer_name, limit=10):
        """
        Get invoices for a specific customer
        
        Args:
            customer_name (str): Customer name
            limit (int): Maximum invoices
            
        Returns:
            list: Customer's invoices
        """
        # First find customer
        customers = self.client.search_customers(name=customer_name, limit=1)
        if not customers:
            return {"error": f"Customer '{customer_name}' not found"}
        
        customer_id = customers[0]['id']
        return self.client.get_invoices(partner_id=customer_id, limit=limit)
    
    # Tool: Get Overdue Invoices
    def get_overdue_invoices(self):
        """
        Get overdue invoices that need immediate attention
        
        Returns:
            list: Overdue invoices sorted by due date
        """
        unpaid = self.client.get_unpaid_invoices(limit=100)
        today = datetime.now().date()
        
        overdue = []
        for invoice in unpaid:
            if invoice.get('invoice_date_due'):
                due_date = datetime.strptime(
                    invoice['invoice_date_due'], '%Y-%m-%d'
                ).date()
                if due_date < today:
                    days_overdue = (today - due_date).days
                    invoice['days_overdue'] = days_overdue
                    overdue.append(invoice)
        
        # Sort by days overdue (most overdue first)
        overdue.sort(key=lambda x: x['days_overdue'], reverse=True)
        return overdue
    
    # Tool: Generate Invoice Report
    def generate_invoice_report(self):
        """
        Generate detailed invoice report for CEO briefing
        
        Returns:
            dict: Comprehensive invoice analytics
        """
        all_invoices = self.client.get_invoices(limit=1000)
        unpaid = self.client.get_unpaid_invoices(limit=1000)
        overdue = self.get_overdue_invoices()
        
        total_revenue = sum(inv['amount_total'] for inv in all_invoices)
        total_unpaid = sum(inv['amount_residual'] for inv in unpaid)
        total_overdue = sum(inv['amount_residual'] for inv in overdue)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_invoices': len(all_invoices),
            'total_revenue': total_revenue,
            'unpaid_count': len(unpaid),
            'unpaid_amount': total_unpaid,
            'overdue_count': len(overdue),
            'overdue_amount': total_overdue,
            'collection_rate': ((total_revenue - total_unpaid) / total_revenue * 100) if total_revenue > 0 else 0,
            'top_overdue': overdue[:5] if overdue else []
        }


def main():
    """MCP Server main entry point"""
    server = OdooMCPServer()
    
    # Example: Handle MCP protocol messages
    # This is a simplified example - adapt to your MCP implementation
    
    while True:
        try:
            # Read request from stdin (MCP protocol)
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            method = request.get('method')
            params = request.get('params', {})
            
            # Route to appropriate tool
            if method == 'get_accounting_summary':
                result = server.get_accounting_summary()
            elif method == 'get_unpaid_invoices':
                result = server.get_unpaid_invoices(**params)
            elif method == 'search_customer':
                result = server.search_customer(**params)
            elif method == 'create_customer':
                result = server.create_customer(**params)
            elif method == 'get_recent_invoices':
                result = server.get_recent_invoices(**params)
            elif method == 'get_customer_invoices':
                result = server.get_customer_invoices(**params)
            elif method == 'get_overdue_invoices':
                result = server.get_overdue_invoices()
            elif method == 'generate_invoice_report':
                result = server.generate_invoice_report()
            else:
                result = {"error": f"Unknown method: {method}"}
            
            # Send response (MCP protocol)
            response = {
                'id': request.get('id'),
                'result': result
            }
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {
                'id': request.get('id') if 'request' in locals() else None,
                'error': str(e)
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
```

## 🔌 Step 2: Register MCP Server

Add to your MCP configuration (e.g., `mcp_config.json`):

```json
{
  "mcpServers": {
    "odoo": {
      "command": "python",
      "args": ["mcp_servers/odoo_server.py"],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "odoo",
        "ODOO_USERNAME": "admin",
        "ODOO_PASSWORD": "secure_admin_password"
      }
    }
  }
}
```

## 🤖 Step 3: Create AI Employee Skills

### Skill: Invoice Follow-up

Create `AI_Employee_Vault/Skills/invoice_followup.md`:

```markdown
# Invoice Follow-up Skill

## Purpose
Automatically identify and follow up on overdue invoices

## Trigger
- Daily at 9 AM
- When new invoice becomes overdue

## Process
1. Get overdue invoices from Odoo
2. For each overdue invoice:
   - Get customer contact info
   - Calculate days overdue
   - Generate follow-up message
   - Create task in Needs_Action
3. Generate summary report

## MCP Tools Used
- odoo.get_overdue_invoices
- odoo.search_customer
- email.send_message (if available)

## Output
- Task files for manual review
- Summary in CEO briefing
```

### Skill: Weekly Accounting Report

Create `AI_Employee_Vault/Skills/weekly_accounting_report.md`:

```markdown
# Weekly Accounting Report Skill

## Purpose
Generate comprehensive weekly accounting summary for CEO

## Trigger
- Every Monday at 8 AM

## Process
1. Get accounting summary from Odoo
2. Generate invoice report
3. Identify trends and issues
4. Create formatted report
5. Save to CEO_Briefings folder

## MCP Tools Used
- odoo.get_accounting_summary
- odoo.generate_invoice_report
- odoo.get_overdue_invoices

## Output Format
```
# Weekly Accounting Report - [Date]

## Summary
- Total Revenue: $X
- Unpaid Amount: $X
- Collection Rate: X%

## Alerts
- X overdue invoices
- Top 3 customers with overdue payments

## Recommendations
[AI-generated recommendations]
```
```

## 🎯 Step 4: Integration with Task Processor

Update `task_processor.py` to use Odoo MCP:

```python
# In your task processor
def process_accounting_task(task):
    """Process accounting-related tasks using Odoo"""
    
    if 'invoice' in task.lower():
        # Get invoice data from Odoo
        invoices = mcp_call('odoo', 'get_unpaid_invoices', {'limit': 10})
        
        # Process and create follow-up tasks
        for invoice in invoices:
            create_followup_task(invoice)
    
    elif 'customer' in task.lower():
        # Search customer in Odoo
        customer_name = extract_customer_name(task)
        customers = mcp_call('odoo', 'search_customer', {'name': customer_name})
        
        # Return customer info
        return format_customer_info(customers)
```

## 📊 Step 5: Dashboard Integration

Update `Dashboard.md` to include Odoo metrics:

```markdown
# Personal AI Employee Dashboard

## Accounting (Odoo)
- Total Customers: {{odoo.customers.total}}
- Unpaid Invoices: {{odoo.invoices.unpaid_count}}
- Unpaid Amount: ${{odoo.invoices.unpaid_amount}}
- Collection Rate: {{odoo.collection_rate}}%

## Recent Activity
{{odoo.recent_invoices}}

## Alerts
{{odoo.overdue_invoices}}
```

## 🔄 Step 6: Automated Workflows

### Workflow 1: Daily Invoice Check

```python
# In scheduler_loop.py or watcher.py
def daily_invoice_check():
    """Check for overdue invoices daily"""
    
    # Get overdue invoices
    overdue = mcp_call('odoo', 'get_overdue_invoices')
    
    if overdue:
        # Create task for each overdue invoice
        for invoice in overdue:
            task_content = f"""
# Invoice Follow-up Required

Customer: {invoice['partner_id'][1]}
Invoice: {invoice['name']}
Amount: ${invoice['amount_residual']}
Days Overdue: {invoice['days_overdue']}

## Action Required
Contact customer for payment follow-up
"""
            create_task_file(task_content, 'Needs_Action')
        
        # Update dashboard
        update_dashboard_metrics()
```

### Workflow 2: Weekly Report Generation

```python
def generate_weekly_report():
    """Generate weekly accounting report"""
    
    # Get comprehensive data
    summary = mcp_call('odoo', 'get_accounting_summary')
    report = mcp_call('odoo', 'generate_invoice_report')
    
    # Format report
    report_content = f"""
# Weekly Accounting Report - {datetime.now().strftime('%Y-%m-%d')}

## Financial Summary
- Total Revenue: ${report['total_revenue']:.2f}
- Unpaid Amount: ${report['unpaid_amount']:.2f}
- Collection Rate: {report['collection_rate']:.1f}%

## Key Metrics
- Total Invoices: {report['total_invoices']}
- Unpaid Count: {report['unpaid_count']}
- Overdue Count: {report['overdue_count']}
- Overdue Amount: ${report['overdue_amount']:.2f}

## Top Overdue Invoices
{format_overdue_list(report['top_overdue'])}

## Recommendations
{generate_recommendations(report)}
"""
    
    # Save to CEO briefings
    save_ceo_briefing(report_content)
```

## 🧪 Testing

Test your integration:

```bash
# 1. Start Odoo
start_odoo.bat

# 2. Test API connection
python odoo_test_api.py

# 3. Test MCP server directly
python mcp_servers/odoo_server.py

# 4. Test from task processor
python task_processor.py
```

## 📋 Available MCP Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `get_accounting_summary` | Overall accounting metrics | None |
| `get_unpaid_invoices` | List unpaid invoices | `limit` |
| `search_customer` | Find customers | `name`, `limit` |
| `create_customer` | Add new customer | `name`, `email`, `phone` |
| `get_recent_invoices` | Recent invoice list | `limit` |
| `get_customer_invoices` | Customer-specific invoices | `customer_name`, `limit` |
| `get_overdue_invoices` | Overdue invoices | None |
| `generate_invoice_report` | Comprehensive report | None |

## 🎓 Best Practices

1. **Error Handling**: Always wrap Odoo calls in try-except
2. **Rate Limiting**: Don't query too frequently
3. **Caching**: Cache summary data for dashboard
4. **Logging**: Log all Odoo operations
5. **Authentication**: Keep credentials in .env
6. **Testing**: Test with sample data first

## 🚀 Next Steps

1. ✅ Start Odoo: `start_odoo.bat`
2. ✅ Test API: `python odoo_test_api.py`
3. ✅ Create MCP server: `mcp_servers/odoo_server.py`
4. ✅ Add skills for accounting automation
5. ✅ Integrate with task processor
6. ✅ Update dashboard with Odoo metrics
7. ✅ Set up automated workflows

## 📚 Resources

- Odoo API: `odoo_integration_example.py`
- Test Script: `odoo_test_api.py`
- Setup Guide: `ODOO_SETUP.md`
- Quick Start: `ODOO_QUICK_START.md`

---

**Your AI Employee is now connected to Odoo for intelligent accounting automation!**
