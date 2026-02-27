#!/usr/bin/env python3
"""
Odoo Community MCP Server - Gold Tier
Provides accounting integration via JSON-RPC API
"""

import json
import logging
import sys
import xmlrpc.client
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

# Logging setup
LOG_PATH = Path("logs/odoo_actions.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [ODOO_SERVER] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class OdooClient:
    """Odoo JSON-RPC client with retry logic and error handling."""

    def __init__(self, url: str, db: str, username: str, password: str):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.common = None
        self.models = None

    def authenticate(self) -> bool:
        """Authenticate with Odoo and get user ID."""
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

            self.uid = self.common.authenticate(self.db, self.username, self.password, {})

            if self.uid:
                logger.info(f"ODOO_AUTH_SUCCESS - User ID: {self.uid}")
                return True
            else:
                logger.error("ODOO_AUTH_FAILED - Invalid credentials")
                return False

        except Exception as e:
            logger.error(f"ODOO_AUTH_ERROR - {str(e)}")
            return False

    def execute_with_retry(self, model: str, method: str, args: list, kwargs: dict = None, max_retries: int = 3) -> Any:
        """Execute Odoo method with retry logic."""
        kwargs = kwargs or {}

        for attempt in range(1, max_retries + 1):
            try:
                result = self.models.execute_kw(
                    self.db, self.uid, self.password,
                    model, method, args, kwargs
                )
                return result

            except xmlrpc.client.Fault as e:
                logger.error(f"ODOO_FAULT - Attempt {attempt}/{max_retries}: {e.faultString}")
                if attempt == max_retries:
                    raise

            except Exception as e:
                logger.error(f"ODOO_ERROR - Attempt {attempt}/{max_retries}: {str(e)}")
                if attempt == max_retries:
                    raise

        return None


class OdooMCPServer:
    """MCP Server for Odoo accounting operations."""

    def __init__(self, url: str = "http://localhost:8069", db: str = "odoo", username: str = "admin", password: str = "admin"):
        self.client = OdooClient(url, db, username, password)
        self.authenticated = False

    def ensure_authenticated(self) -> bool:
        """Ensure client is authenticated before operations."""
        if not self.authenticated:
            self.authenticated = self.client.authenticate()
        return self.authenticated

    def get_unpaid_invoices(self) -> Dict[str, Any]:
        """Get all unpaid customer invoices."""
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info("ODOO_QUERY - Fetching unpaid invoices")

            # Search for unpaid invoices (state = 'posted', payment_state != 'paid')
            invoice_ids = self.client.execute_with_retry(
                'account.move',
                'search',
                [[
                    ('move_type', '=', 'out_invoice'),
                    ('state', '=', 'posted'),
                    ('payment_state', 'in', ['not_paid', 'partial'])
                ]]
            )

            if not invoice_ids:
                logger.info("ODOO_RESULT - No unpaid invoices found")
                return {"success": True, "invoices": [], "count": 0}

            # Read invoice details
            invoices = self.client.execute_with_retry(
                'account.move',
                'read',
                [invoice_ids],
                {'fields': ['name', 'partner_id', 'amount_total', 'amount_residual', 'invoice_date', 'invoice_date_due', 'payment_state']}
            )

            logger.info(f"ODOO_SUCCESS - Found {len(invoices)} unpaid invoices")

            return {
                "success": True,
                "invoices": invoices,
                "count": len(invoices),
                "total_outstanding": sum(inv['amount_residual'] for inv in invoices)
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - get_unpaid_invoices failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def create_invoice(self, partner_name: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new customer invoice.

        Args:
            partner_name: Customer name
            items: List of dicts with 'product', 'quantity', 'price'
        """
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info(f"ODOO_CREATE - Creating invoice for {partner_name}")

            # Find partner by name
            partner_ids = self.client.execute_with_retry(
                'res.partner',
                'search',
                [[('name', 'ilike', partner_name)]],
                {'limit': 1}
            )

            if not partner_ids:
                logger.error(f"ODOO_ERROR - Partner not found: {partner_name}")
                return {"success": False, "error": f"Partner '{partner_name}' not found"}

            partner_id = partner_ids[0]

            # Prepare invoice lines
            invoice_lines = []
            for item in items:
                # Find product
                product_ids = self.client.execute_with_retry(
                    'product.product',
                    'search',
                    [[('name', 'ilike', item['product'])]],
                    {'limit': 1}
                )

                if not product_ids:
                    logger.warning(f"ODOO_WARNING - Product not found: {item['product']}, skipping")
                    continue

                invoice_lines.append((0, 0, {
                    'product_id': product_ids[0],
                    'quantity': item.get('quantity', 1),
                    'price_unit': item.get('price', 0),
                }))

            if not invoice_lines:
                return {"success": False, "error": "No valid invoice lines"}

            # Create invoice
            invoice_id = self.client.execute_with_retry(
                'account.move',
                'create',
                [{
                    'move_type': 'out_invoice',
                    'partner_id': partner_id,
                    'invoice_date': datetime.now().strftime('%Y-%m-%d'),
                    'invoice_line_ids': invoice_lines
                }]
            )

            # Read created invoice
            invoice = self.client.execute_with_retry(
                'account.move',
                'read',
                [[invoice_id]],
                {'fields': ['name', 'amount_total', 'state']}
            )[0]

            logger.info(f"ODOO_SUCCESS - Invoice created: {invoice['name']}, Amount: {invoice['amount_total']}")

            return {
                "success": True,
                "invoice_id": invoice_id,
                "invoice_number": invoice['name'],
                "amount": invoice['amount_total'],
                "state": invoice['state']
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - create_invoice failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def record_payment(self, invoice_id: int, amount: float, payment_date: str = None) -> Dict[str, Any]:
        """Record a payment against an invoice."""
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info(f"ODOO_PAYMENT - Recording payment for invoice {invoice_id}")

            payment_date = payment_date or datetime.now().strftime('%Y-%m-%d')

            # Create payment
            payment_id = self.client.execute_with_retry(
                'account.payment',
                'create',
                [{
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'amount': amount,
                    'date': payment_date,
                    'ref': f'Payment for invoice {invoice_id}'
                }]
            )

            # Post the payment
            self.client.execute_with_retry(
                'account.payment',
                'action_post',
                [[payment_id]]
            )

            logger.info(f"ODOO_SUCCESS - Payment recorded: ID {payment_id}, Amount: {amount}")

            return {
                "success": True,
                "payment_id": payment_id,
                "amount": amount,
                "date": payment_date
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - record_payment failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_weekly_revenue(self, weeks_back: int = 1) -> Dict[str, Any]:
        """Get revenue for the past N weeks."""
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info(f"ODOO_QUERY - Fetching revenue for past {weeks_back} weeks")

            start_date = (datetime.now() - timedelta(weeks=weeks_back)).strftime('%Y-%m-%d')

            # Search paid invoices in date range
            invoice_ids = self.client.execute_with_retry(
                'account.move',
                'search',
                [[
                    ('move_type', '=', 'out_invoice'),
                    ('state', '=', 'posted'),
                    ('invoice_date', '>=', start_date),
                    ('payment_state', '=', 'paid')
                ]]
            )

            if not invoice_ids:
                logger.info("ODOO_RESULT - No revenue in period")
                return {"success": True, "revenue": 0, "invoice_count": 0}

            invoices = self.client.execute_with_retry(
                'account.move',
                'read',
                [invoice_ids],
                {'fields': ['amount_total', 'invoice_date']}
            )

            total_revenue = sum(inv['amount_total'] for inv in invoices)

            logger.info(f"ODOO_SUCCESS - Weekly revenue: {total_revenue} from {len(invoices)} invoices")

            return {
                "success": True,
                "revenue": total_revenue,
                "invoice_count": len(invoices),
                "period_start": start_date,
                "period_end": datetime.now().strftime('%Y-%m-%d')
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - get_weekly_revenue failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_cashflow_summary(self) -> Dict[str, Any]:
        """Get current cashflow summary."""
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info("ODOO_QUERY - Fetching cashflow summary")

            # Get accounts receivable (unpaid invoices)
            unpaid_result = self.get_unpaid_invoices()
            accounts_receivable = unpaid_result.get('total_outstanding', 0) if unpaid_result['success'] else 0

            # Get this month's revenue
            revenue_result = self.get_weekly_revenue(weeks_back=4)
            monthly_revenue = revenue_result.get('revenue', 0) if revenue_result['success'] else 0

            logger.info(f"ODOO_SUCCESS - Cashflow: AR={accounts_receivable}, Revenue={monthly_revenue}")

            return {
                "success": True,
                "accounts_receivable": accounts_receivable,
                "monthly_revenue": monthly_revenue,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - get_cashflow_summary failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def reconcile_bank_transactions(self) -> Dict[str, Any]:
        """Get unreconciled bank transactions."""
        try:
            if not self.ensure_authenticated():
                return {"success": False, "error": "Authentication failed"}

            logger.info("ODOO_QUERY - Fetching unreconciled transactions")

            # Search for unreconciled bank statement lines
            line_ids = self.client.execute_with_retry(
                'account.bank.statement.line',
                'search',
                [[('is_reconciled', '=', False)]]
            )

            if not line_ids:
                logger.info("ODOO_RESULT - No unreconciled transactions")
                return {"success": True, "transactions": [], "count": 0}

            lines = self.client.execute_with_retry(
                'account.bank.statement.line',
                'read',
                [line_ids],
                {'fields': ['date', 'payment_ref', 'amount', 'partner_id']}
            )

            logger.info(f"ODOO_SUCCESS - Found {len(lines)} unreconciled transactions")

            return {
                "success": True,
                "transactions": lines,
                "count": len(lines)
            }

        except Exception as e:
            logger.error(f"ODOO_ERROR - reconcile_bank_transactions failed: {str(e)}")
            return {"success": False, "error": str(e)}


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming MCP requests."""

    # Initialize server (credentials should come from .env in production)
    server = OdooMCPServer(
        url="http://localhost:8069",
        db="odoo",
        username="admin",
        password="admin"
    )

    action = request.get('action')
    params = request.get('params', {})

    if action == 'get_unpaid_invoices':
        return server.get_unpaid_invoices()

    elif action == 'create_invoice':
        return server.create_invoice(
            partner_name=params.get('partner_name'),
            items=params.get('items', [])
        )

    elif action == 'record_payment':
        return server.record_payment(
            invoice_id=params.get('invoice_id'),
            amount=params.get('amount'),
            payment_date=params.get('payment_date')
        )

    elif action == 'get_weekly_revenue':
        return server.get_weekly_revenue(
            weeks_back=params.get('weeks_back', 1)
        )

    elif action == 'get_cashflow_summary':
        return server.get_cashflow_summary()

    elif action == 'reconcile_bank_transactions':
        return server.reconcile_bank_transactions()

    else:
        return {"success": False, "error": f"Unknown action: {action}"}


def main():
    """MCP Server main loop."""
    logger.info("ODOO_SERVER_STARTED - Listening for MCP requests")

    try:
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = handle_mcp_request(request)
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                error_response = {"success": False, "error": f"Invalid JSON: {str(e)}"}
                print(json.dumps(error_response), flush=True)

            except Exception as e:
                error_response = {"success": False, "error": f"Server error: {str(e)}"}
                print(json.dumps(error_response), flush=True)
                logger.error(f"ODOO_SERVER_ERROR - {str(e)}")

    except KeyboardInterrupt:
        logger.info("ODOO_SERVER_STOPPED - User interrupt")


if __name__ == "__main__":
    main()
