#!/usr/bin/env python3
"""
Odoo XML-RPC API Test Script
Tests connection and basic operations with Odoo instance
"""

import xmlrpc.client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'secure_admin_password')


def test_odoo_connection():
    """Test Odoo XML-RPC connection and authentication"""
    
    print("=" * 60)
    print("ODOO XML-RPC API CONNECTION TEST")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  URL: {ODOO_URL}")
    print(f"  Database: {ODOO_DB}")
    print(f"  Username: {ODOO_USERNAME}")
    print(f"  Password: {'*' * len(ODOO_PASSWORD)}")
    print()
    
    try:
        # Test 1: Common endpoint (version info)
        print("[1/5] Testing common endpoint...")
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        version_info = common.version()
        print(f"✓ Connected to Odoo {version_info['server_version']}")
        print(f"  Server version: {version_info['server_version']}")
        print(f"  Protocol version: {version_info['protocol_version']}")
        print()
        
        # Test 2: Authentication
        print("[2/5] Testing authentication...")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        if uid:
            print(f"✓ Authentication successful (User ID: {uid})")
        else:
            print("✗ Authentication failed")
            return False
        print()
        
        # Test 3: Object endpoint
        print("[3/5] Testing object endpoint...")
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
        print("✓ Object endpoint accessible")
        print()
        
        # Test 4: Read user info
        print("[4/5] Reading user information...")
        user_data = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [uid], {'fields': ['name', 'login', 'email', 'company_id']}
        )
        if user_data:
            print(f"✓ User data retrieved:")
            print(f"  Name: {user_data[0].get('name')}")
            print(f"  Login: {user_data[0].get('login')}")
            print(f"  Email: {user_data[0].get('email', 'Not set')}")
            print(f"  Company: {user_data[0].get('company_id', ['N/A'])[1] if user_data[0].get('company_id') else 'N/A'}")
        print()
        
        # Test 5: Check available models
        print("[5/5] Checking available models...")
        model_access = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ir.model', 'search_read',
            [[('model', 'in', ['res.partner', 'account.move', 'sale.order'])]],
            {'fields': ['model', 'name'], 'limit': 10}
        )
        print(f"✓ Found {len(model_access)} key models:")
        for model in model_access:
            print(f"  - {model['model']}: {model['name']}")
        print()
        
        # Success summary
        print("=" * 60)
        print("✓ ALL TESTS PASSED - Odoo API is ready!")
        print("=" * 60)
        print("\nYou can now integrate Odoo with your Python backend.")
        print("Example usage:")
        print("""
# Create a partner (customer/contact)
partner_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'create',
    [{'name': 'John Doe', 'email': 'john@example.com'}]
)

# Search partners
partners = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'search_read',
    [[('is_company', '=', True)]],
    {'fields': ['name', 'email'], 'limit': 5}
)
        """)
        
        return True
        
    except xmlrpc.client.ProtocolError as e:
        print(f"✗ Protocol Error: {e}")
        print("  Make sure Odoo is running at the correct URL")
        return False
    except ConnectionRefusedError:
        print("✗ Connection Refused")
        print("  Make sure Odoo container is running: docker-compose ps")
        return False
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = test_odoo_connection()
    exit(0 if success else 1)
