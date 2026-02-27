#!/usr/bin/env python3
"""
Gold Tier Validation Script
Tests all MCP servers and generates a system health report
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 60)
print("  Digital FTE - Gold Tier Validation")
print("=" * 60)
print()

results = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "passed": 0,
    "failed": 0
}

def test_component(name, test_func):
    """Run a test and record results."""
    print(f"Testing {name}...", end=" ")
    try:
        test_func()
        print("[PASS]")
        results["tests"].append({"name": name, "status": "PASS"})
        results["passed"] += 1
        return True
    except Exception as e:
        print(f"[FAIL]: {str(e)}")
        results["tests"].append({"name": name, "status": "FAIL", "error": str(e)})
        results["failed"] += 1
        return False

# Test 1: Directory Structure
def test_directories():
    required_dirs = [
        "AI_Employee_Vault/Inbox",
        "AI_Employee_Vault/Needs_Action",
        "AI_Employee_Vault/Done",
        "AI_Employee_Vault/Plans",
        "AI_Employee_Vault/Skills",
        "AI_Employee_Vault/CEO_Briefings",
        "mcp_servers",
        "scripts",
        "logs"
    ]
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            raise FileNotFoundError(f"Missing directory: {dir_path}")

test_component("Directory Structure", test_directories)

# Test 2: MCP Servers Exist
def test_mcp_servers():
    required_servers = [
        "mcp_servers/odoo_server.py",
        "mcp_servers/facebook_server.py",
        "mcp_servers/instagram_server.py",
        "mcp_servers/twitter_server.py",
        "mcp_servers/email_server.py",
        "mcp_servers/linkedin_server.py",
        "mcp_servers/whatsapp_server.py",
        "mcp_servers/vault_watcher_server.py",
        "mcp_servers/gmail_server.py"
    ]
    for server in required_servers:
        if not Path(server).exists():
            raise FileNotFoundError(f"Missing MCP server: {server}")

test_component("MCP Servers", test_mcp_servers)

# Test 3: Skills Exist
def test_skills():
    required_skills = [
        "AI_Employee_Vault/Skills/odoo_accounting_manager.md",
        "AI_Employee_Vault/Skills/invoice_reconciliation.md",
        "AI_Employee_Vault/Skills/facebook_poster.md",
        "AI_Employee_Vault/Skills/facebook_engagement_analyzer.md",
        "AI_Employee_Vault/Skills/instagram_poster.md",
        "AI_Employee_Vault/Skills/instagram_growth_analyzer.md",
        "AI_Employee_Vault/Skills/twitter_poster.md",
        "AI_Employee_Vault/Skills/twitter_engagement_analyzer.md"
    ]
    for skill in required_skills:
        if not Path(skill).exists():
            raise FileNotFoundError(f"Missing skill: {skill}")

test_component("Gold Tier Skills", test_skills)

# Test 4: CEO Briefing Generator
def test_ceo_briefing():
    briefing_script = Path("scripts/ceo_briefing_generator.py")
    if not briefing_script.exists():
        raise FileNotFoundError("CEO Briefing generator not found")

    # Check if CEO_Briefings directory exists
    briefing_dir = Path("AI_Employee_Vault/CEO_Briefings")
    if not briefing_dir.exists():
        raise FileNotFoundError("CEO_Briefings directory not found")

test_component("CEO Briefing System", test_ceo_briefing)

# Test 5: Core Watchers
def test_watchers():
    required_watchers = [
        "AI_Employee_Vault/watcher.py",
        "AI_Employee_Vault/reasoning_engine.py",
        "scripts/gmail_watcher.py",
        "scripts/linkedin_watcher.py",
        "scripts/whatsapp_watcher.py"
    ]
    for watcher in required_watchers:
        if not Path(watcher).exists():
            raise FileNotFoundError(f"Missing watcher: {watcher}")

test_component("Core Watchers", test_watchers)

# Test 6: Documentation
def test_documentation():
    required_docs = [
        "README.md",
        "GOLD_TIER_DOCUMENTATION.md",
        "SCHEDULER_SETUP.md"
    ]
    for doc in required_docs:
        if not Path(doc).exists():
            raise FileNotFoundError(f"Missing documentation: {doc}")

test_component("Documentation", test_documentation)

# Test 7: Startup Scripts
def test_startup_scripts():
    if not Path("start_gold_tier.bat").exists():
        raise FileNotFoundError("Gold Tier startup script not found")

test_component("Startup Scripts", test_startup_scripts)

# Test 8: Python Imports
def test_imports():
    try:
        import requests
        import watchdog
        import google.auth
    except ImportError as e:
        raise ImportError(f"Missing Python dependency: {e}")

test_component("Python Dependencies", test_imports)

# Test 9: Log Directory
def test_logs():
    log_dir = Path("logs")
    if not log_dir.exists():
        raise FileNotFoundError("Logs directory not found")

test_component("Logging System", test_logs)

# Test 10: Configuration Files
def test_config():
    if not Path("requirements.txt").exists():
        raise FileNotFoundError("requirements.txt not found")

test_component("Configuration Files", test_config)

# Print Summary
print()
print("=" * 60)
print("  Validation Summary")
print("=" * 60)
print()
print(f"Total Tests: {results['passed'] + results['failed']}")
print(f"[PASS] Passed: {results['passed']}")
print(f"[FAIL] Failed: {results['failed']}")
print()

if results['failed'] == 0:
    print("SUCCESS! All tests passed! Gold Tier is ready.")
    print()
    print("Next Steps:")
    print("1. Configure API credentials in .env file")
    print("2. Set up Odoo Community Edition")
    print("3. Configure Claude Desktop MCP servers")
    print("4. Run: start_gold_tier.bat")
    print("5. Generate first CEO Briefing: python scripts/ceo_briefing_generator.py")
    exit_code = 0
else:
    print("WARNING: Some tests failed. Please fix the issues above.")
    print()
    print("Failed Tests:")
    for test in results['tests']:
        if test['status'] == 'FAIL':
            print(f"  - {test['name']}: {test.get('error', 'Unknown error')}")
    exit_code = 1

# Save results
results_file = Path("logs/gold_tier_validation.json")
results_file.parent.mkdir(parents=True, exist_ok=True)
with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print(f"Detailed results saved to: {results_file}")
print()

sys.exit(exit_code)
