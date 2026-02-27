#!/usr/bin/env python3
"""
Odoo Integration Example for Personal AI Employee
Demonstrates common operations for accounting automation
"""

import xmlrpc.client
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class OdooClient:
    """Simple Odoo XML-RPC client wrapper"""
    
    def __init__(self):
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo')
        self.username = os.getenv('ODOO_USERNAME', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', 'secure_admin_password')
        
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        self.uid = None
        
    def authenticate(self):
        """Authenticate with Odoo"""
        self.uid = self.common.authenticate(
            self.db, self.username, self.password, {}
        )
        return self.uid
    
    def execute(self, model, method, *args, **kwargs):
        """Execute a method on an Odoo model"""
        if not self.uid:
            self.authenticate()
        
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, method, args, kwargs
        )
    
    # Customer/Partner Operations
    def create_customer(self, name, email=None, phone=None, is_company=False):
        """Create a new customer/partner"""
        vals = {
            'name': name,
            'is_company': is_company,
            'customer_rank': 1,
        }
        if email:
            vals['email'] = email
        if phone:
            vals['phone'] = phone
            
        return self.execute('res.partner', 'create', [vals])
    
    def search_customers(self, name=None, limit=10):
        """Search for customers"""
        domain = [('customer_rank', '>', 0)]
        if name:
            domain.append(('name', 'ilike', name))
            
        return self.execute(
            'res.partner', 'search_read',
            [domain],
            {'fields': ['name', 'email', 'phone'], 'limit': limit}
        )
    
    # Invoice Operations
    def get_invoices(self, state=None, partner_id=None, limit=10):
        """Get invoices with optional filters"""
        domain = [('move_type', '=', 'out_invoice')]
        
        if state:
            domain.append(('state', '=', state))
        if partner_id:
            domain.append(('partner_id', '=', partner_id))
            
        return self.execute(
            'account.move', 'search_read',
            [domain],
            {
                'fields': [
                    'name', 'partner_id', 'invoice_date',
                    'amount_total', 'amount_residual', 'state'
                ],
                'limit': limit,
                'order': 'invoice_date desc'
            }
        )
    
    def get_unpaid_invoices(self, limit=10):
        """Get all unpaid invoices"""
        return self.execute(
            'account.move', 'search_read',
            [[
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial'])
            ]],
            {
                'fields': [
                    'name', 'partner_id', 'invoice_date',
                    'invoice_date_due', 'amount_total',
                    'amount_residual', 'payment_state'
                ],
                'limit': limit,
                'order': 'invoice_date_due asc'
            }
        )
    
    # Payment Operations
    def get_payments(self, partner_id=None, limit=10):
        """Get payment records"""
        domain = []
        if partner_id:
            domain.append(('partner_id', '=', partner_id))
            
        return self.execute(
            'account.payment', 'search_read',
            [domain],
            {
                'fields': [
                    'name', 'partner_id', 'date',
                    'amount', 'state', 'payment_type'
                ],
                'limit': limit,
                'order': 'date desc'
            }
        )
    
    # Product Operations
    def search_products(self, name=None, limit=10):
        """Search for products"""
        domain = []
        if name:
            domain.append(('name', 'ilike', name))
            
        return self.execute(
            'product.product', 'search_read',
            [domain],
            {
                'fields': ['name', 'list_price', 'standard_price', 'qty_available'],
                'limit': limit
            }
        )
    
    # Reporting
    def get_accounting_summary(self):
        """Get accounting summary for AI Employee dashboard"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'customers': {},
            'invoices': {},
            'payments': {}
        }
        
        # Customer count
        customer_count = self.execute(
            'res.partner', 'search_count',
            [[('customer_rank', '>', 0)]]
        )
        summary['customers']['total'] = customer_count
        
        # Invoice statistics
        all_invoices = self.execute(
            'account.move', 'search_count',
            [[('move_type', '=', 'out_invoice')]]
        )
        draft_invoices = self.execute(
            'account.move', 'search_count',
            [[('move_type', '=', 'out_invoice'), ('state', '=', 'draft')]]
        )
        posted_invoices = self.execute(
            'account.move', 'search_count',
            [[('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]]
        )
        
        summary['invoices']['total'] = all_invoices
        summary['invoices']['draft'] = draft_invoices
        summary['invoices']['posted'] = posted_invoices
        
        # Unpaid invoices
        unpaid = self.get_unpaid_invoices(limit=100)
        total_unpaid = sum(inv['amount_residual'] for inv in unpaid)
        
        summary['invoices']['unpaid_count'] = len(unpaid)
        summary['invoices']['unpaid_amount'] = total_unpaid
        
        return summary


def demo():
    """Demonstration of Odoo integration"""
    print("=" * 60)
    print("ODOO INTEGRATION DEMO")
    print("=" * 60)
    print()
    
    # Initialize client
    client = OdooClient()
    
    print("Authenticating...")
    if not client.authenticate():
        print("✗ Authentication failed")
        return
    print(f"✓ Authenticated (User ID: {client.uid})")
    print()
    
    # Get accounting summary
    print("Fetching accounting summary...")
    summary = client.get_accounting_summary()
    print(f"✓ Summary generated")
    print()
    
    print("ACCOUNTING SUMMARY")
    print("-" * 60)
    print(f"Customers: {summary['customers']['total']}")
    print(f"Total Invoices: {summary['invoices']['total']}")
    print(f"  - Draft: {summary['invoices']['draft']}")
    print(f"  - Posted: {summary['invoices']['posted']}")
    print(f"Unpaid Invoices: {summary['invoices']['unpaid_count']}")
    print(f"Unpaid Amount: ${summary['invoices']['unpaid_amount']:.2f}")
    print()
    
    # Search customers
    print("Recent Customers:")
    print("-" * 60)
    customers = client.search_customers(limit=5)
    for customer in customers:
        print(f"  - {customer['name']}")
        if customer.get('email'):
            print(f"    Email: {customer['email']}")
    print()
    
    # Get unpaid invoices
    print("Unpaid Invoices (Top 5):")
    print("-" * 60)
    unpaid = client.get_unpaid_invoices(limit=5)
    for invoice in unpaid:
        partner_name = invoice['partner_id'][1] if invoice['partner_id'] else 'N/A'
        print(f"  - {invoice['name']}: ${invoice['amount_residual']:.2f}")
        print(f"    Customer: {partner_name}")
        print(f"    Due: {invoice.get('invoice_date_due', 'N/A')}")
    print()
    
    print("=" * 60)
    print("✓ Demo completed successfully!")
    print("=" * 60)
    print()
    print("Integration ready for Personal AI Employee system.")


if __name__ == "__main__":
    demo()
