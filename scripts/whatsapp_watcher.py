import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
CHECK_INTERVAL = 60  # seconds
LOG_PATH = "logs/whatsapp_actions.log"
PROCESSED_IDS_FILE = "whatsapp_processed.json"
INBOUND_FILE = "whatsapp_inbound.json"
INBOX_PATH = Path("AI_Employee_Vault/Inbox")

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
INBOX_PATH.mkdir(parents=True, exist_ok=True)


def log_event(event, level="INFO"):
    """Log event with standardized prefixes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [WHATSAPP_WATCHER] ACTION - {event}"
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")


def load_processed_ids():
    """Load processed WhatsApp message IDs."""
    if os.path.exists(PROCESSED_IDS_FILE):
        try:
            with open(PROCESSED_IDS_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("processed_ids", []))
        except (json.JSONDecodeError, FileNotFoundError):
            return set()
    return set()


def save_processed_id(msg_id):
    """Save processed message ID."""
    processed = load_processed_ids()
    processed.add(msg_id)
    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump({"processed_ids": list(processed)}, f, indent=2)


def fetch_whatsapp_messages():
    """Fetch messages from the mock source (whatsapp_inbound.json)."""
    if not os.path.exists(INBOUND_FILE):
        return []
    
    try:
        with open(INBOUND_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("messages", [])
    except Exception as e:
        log_event(f"WHATSAPP_ERROR - Failed to read inbound file: {e}")
        return []


def trigger_claude_scheduler():
    """Trigger the Reasoning Engine via Claude Scheduler with 3 retries."""
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            log_event(f"WHATSAPP_TRIGGERED - Executing: claude scheduler --once (Attempt {attempt})")
            # Use shell=True for Windows and ensure 'claude' is in PATH or mocked
            result = subprocess.run(["claude", "scheduler", "--once"], capture_output=True, text=True, shell=True, timeout=30)
            
            if result.returncode == 0:
                return True
            else:
                log_event(f"WHATSAPP_ERROR - Trigger failed with code {result.returncode}: {result.stderr}", "ERROR")
        except subprocess.TimeoutExpired:
            log_event(f"WHATSAPP_ERROR - Trigger timed out on attempt {attempt}", "ERROR")
        except Exception as e:
            log_event(f"WHATSAPP_ERROR - Trigger failed on attempt {attempt}: {e}", "ERROR")
        
        if attempt < max_retries:
            time.sleep(2)  # Backoff before retry
            
    log_event("WHATSAPP_ERROR - Trigger failed after maximum retries", "ERROR")
    return False


def create_task_from_whatsapp(sender, message, timestamp, chat_id):
    """Create a v1.0 Silver Tier structured task file."""
    try:
        INBOX_PATH.mkdir(parents=True, exist_ok=True)

        task_content = f"""# WhatsApp Event

Sender: {sender}
Message: {message}
Timestamp: {timestamp}
Risk Level: Medium
"""

        filename = f"whatsapp-{chat_id}.md"
        task_file = INBOX_PATH / filename

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)

        log_event(f"WHATSAPP_NEW - Received from {sender} (Chat ID: {chat_id})")
        return task_file

    except Exception as e:
        log_event(f"WHATSAPP_ERROR - Failed to create task file: {e}")
        return None


def watch_whatsapp():
    """Main WhatsApp watching loop - v1.0 Silver Tier."""
    log_event("WHATSAPP WATCHER STARTED - v1.0 Silver Tier")

    while True:
        try:
            processed_ids = load_processed_ids()
            messages = fetch_whatsapp_messages()

            if messages:
                for msg in messages:
                    msg_id = msg.get('id')
                    chat_id = msg.get('chat_id')
                    
                    if not msg_id or msg_id in processed_ids:
                        continue

                    task_file = create_task_from_whatsapp(
                        msg.get('sender'),
                        msg.get('message'),
                        msg.get('timestamp'),
                        chat_id
                    )

                    if task_file:
                        save_processed_id(msg_id)
                        trigger_claude_scheduler()

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log_event("WHATSAPP WATCHER STOPPED - User interrupt")
            break
        except Exception as e:
            log_event(f"WHATSAPP_ERROR - {str(e)}")
            time.sleep(10)


if __name__ == "__main__":
    watch_whatsapp()
