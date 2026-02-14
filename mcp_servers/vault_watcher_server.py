import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Path Configuration
VAULT_ROOT = Path("AI_Employee_Vault")
INBOX_PATH = VAULT_ROOT / "Inbox"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
DONE_PATH = VAULT_ROOT / "Done"
LOG_PATH = "logs/actions.log"

def log_event(event):
    """Standardized timestamped logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [VAULT_WATCHER] ACTION - {event}"
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")

def get_vault_stats():
    """Return counts of files in each folder."""
    stats = {
        "Inbox": len(list(INBOX_PATH.glob("*.md"))),
        "Needs_Action": len(list(NEEDS_ACTION_PATH.glob("*.md"))),
        "Done": len(list(DONE_PATH.glob("*.md")))
    }
    return stats

def trigger_rescan():
    """Trigger a reasoning engine run via Claude Scheduler."""
    try:
        log_event("Triggering claude scheduler --once")
        # Ensure 'claude' is in PATH or provide full path if known
        result = subprocess.run(["claude", "scheduler", "--once"], capture_output=True, text=True, shell=True)
        return f"Rescan triggered: {result.stdout[:50]}"
    except Exception as e:
        log_event(f"Rescan trigger failed: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    pass
