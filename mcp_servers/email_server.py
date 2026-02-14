import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Path Configuration
VAULT_ROOT = Path("AI_Employee_Vault")
PLANS_PATH = VAULT_ROOT / "Plans"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
SENT_EMAILS_FILE = "sent_emails.json"
LOG_PATH = "logs/gmail_actions.log"

def log_event(event):
    """Standardized timestamped logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [EMAIL_SERVER] ACTION - {event}"
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
    """Check if the plan allows for execution based on risk and approval."""
    try:
        content = plan_path.read_text(encoding='utf-8')
        content_lower = content.lower()
        
        # Mandatory Plan fields
        if not all(field in content_lower for field in ["goal:", "risk level:", "approval status:"]):
            return False, "Missing mandatory Plan fields"

        # Approval logic
        if "risk level: high" in content_lower or "risk level: medium" in content_lower:
            if "approval status: approved" not in content_lower:
                return False, "Risk level requires explicit 'Approved' status"
                
        return True, "Validated"
    except Exception as e:
        return False, f"Validation error: {e}"

def send_email(recipient, subject, body):
    """MCP Capability: send_email (Simulated)."""
    # Validation check first
    plan = get_latest_plan()
    if not plan:
        log_event("No Plan.md found")
        return "Error: No Plan found"

    is_valid, msg = validate_approval(plan)
    if not is_valid:
        log_event(f"{msg}")
        return f"Error: {msg}"

    # Duplicate protection
    if os.path.exists(SENT_EMAILS_FILE):
        try:
            with open(SENT_EMAILS_FILE, 'r') as f:
                sent = json.load(f).get("sent", [])
                if f"{recipient}:{subject}" in sent:
                    log_event(f"Duplicate detected for {recipient}")
                    return "Error: Duplicate email"
        except Exception: pass

    # Execution
    log_event(f"Sending email to {recipient}")
    # Update sent history
    sent = []
    if os.path.exists(SENT_EMAILS_FILE):
        try:
            with open(SENT_EMAILS_FILE, 'r') as f:
                sent = json.load(f).get("sent", [])
        except Exception: pass
    sent.append(f"{recipient}:{subject}")
    with open(SENT_EMAILS_FILE, 'w') as f:
        json.dump({"sent": sent}, f)
        
    return "Success"

if __name__ == "__main__":
    pass
