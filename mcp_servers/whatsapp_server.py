import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Path Configuration
VAULT_ROOT = Path("AI_Employee_Vault")
PLANS_PATH = VAULT_ROOT / "Plans"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
LOG_PATH = "logs/whatsapp_actions.log"

def log_event(event):
    """Standardized timestamped logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [WHATSAPP_SERVER] ACTION - {event}"
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")

def get_latest_plan():
    """Find the most recent plan in either Plans/ or Needs_Action/."""
    plans = list(PLANS_PATH.glob("*.md")) + list(NEEDS_ACTION_PATH.glob("*.md"))
    if not plans:
        return None
    return max(plans, key=os.path.getmtime)

def validate_approval(plan_path):
    """Check if the plan allows for execution."""
    try:
        content = plan_path.read_text(encoding='utf-8')
        content_lower = content.lower()
        
        if "risk level: low" in content_lower:
            return True, "Validated"

        if "approval status: approved" in content_lower:
            return True, "Validated"
            
        return False, "Approval required for risk > Low"
    except Exception as e:
        return False, f"Validation error: {e}"

def send_message(to, text):
    """MCP Capability: send_message (Simulated)."""
    plan = get_latest_plan()
    if not plan:
        log_event("No Plan.md found")
        return "Error: No Plan found"

    is_valid, msg = validate_approval(plan)
    if not is_valid:
        log_event(f"{msg}")
        return f"Error: {msg}"

    # Execution
    log_event(f"Sending WhatsApp message to {to}")
    return "Success"

if __name__ == "__main__":
    pass
