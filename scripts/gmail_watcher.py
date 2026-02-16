import os
import time
import pickle
import sys
import subprocess
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Try to import notification library
try:
    from plyer import notification as plyer_notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    plyer_notification = None

# Configuration
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly'
]
CHECK_INTERVAL = 60  # seconds - v2.0 Silver Tier
LOG_PATH = "logs/gmail_actions.log"
TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials.json"
PROCESSED_IDS_FILE = "processed_ids.json"
INBOX_PATH = Path("AI_Employee_Vault/Inbox")

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
INBOX_PATH.mkdir(parents=True, exist_ok=True)


def log_event(event):
    """Log event to gmail_actions.log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [GMAIL_WATCHER] ACTION - {event}"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")


def load_processed_ids():
    """Load set of already processed email IDs from JSON."""
    if os.path.exists(PROCESSED_IDS_FILE):
        try:
            with open(PROCESSED_IDS_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("processed_ids", []))
        except (json.JSONDecodeError, FileNotFoundError):
            return set()
    return set()


def save_processed_id(email_id):
    """Save processed email ID to JSON file."""
    processed = load_processed_ids()
    processed.add(email_id)

    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump({"processed_ids": list(processed)}, f, indent=2)


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                log_event(f"GMAIL_ERROR - Token refresh failed: {str(e)}")
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_PATH):
                log_event(f"GMAIL_ERROR - credentials.json not found.")
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_PATH}. Download OAuth2 credentials from Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def get_unread_messages(service):
    """Fetch unread messages from INBOX."""
    try:
        # v2.0 Silver Tier: Focus on INBOX
        results = service.users().messages().list(
            userId='me',
            q='is:unread label:INBOX',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])
        return messages

    except HttpError as error:
        log_event(f"GMAIL_ERROR - Gmail API error: {error}")
        return []


def get_message_details(service, msg_id):
    """Get email subject, sender, and body snippet."""
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = message.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        snippet = message.get('snippet', 'No content preview available')

        return msg_id, sender, subject, snippet, date

    except HttpError as error:
        log_event(f"GMAIL_ERROR - Failed to get message details: {error}")
        return msg_id, "Unknown", "Unknown", "No content", "Unknown"


def create_task_from_email(message_id, sender, subject, summary, date):
    """Create a structured task file in Inbox folder."""
    try:
        INBOX_PATH.mkdir(parents=True, exist_ok=True)

        task_content = f"""# Gmail Event

Sender: {sender}
Subject: {subject}
Summary: {summary}
Timestamp: {date}
Risk Level: Low
"""

        filename = f"gmail-{message_id}.md"
        task_file = INBOX_PATH / filename

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)

        log_event(f"GMAIL_NEW - {subject[:50]}")
        return task_file

    except Exception as e:
        log_event(f"GMAIL_ERROR - Failed to create task file: {e}")
        return None

def trigger_claude_scheduler():
    """Trigger the Reasoning Engine via Claude Scheduler."""
    try:
        log_event("Executing: claude scheduler --once")
        result = subprocess.run(["claude", "scheduler", "--once"], capture_output=True, text=True, shell=True)
        return True
    except Exception as e:
        log_event(f"Trigger failed: {e}")
        return False


def watch_gmail():
    """Main Gmail watching loop - v2.0 Silver Tier."""
    log_event("GMAIL WATCHER STARTED - v2.0 Silver Tier")

    try:
        service = get_gmail_service()
        log_event("Gmail API authenticated successfully")
    except Exception as e:
        log_event(f"GMAIL_ERROR - Failed to authenticate: {str(e)}")
        return

    processed_ids = load_processed_ids()
    log_event(f"Loaded {len(processed_ids)} previously processed email IDs")

    while True:
        try:
            messages = get_unread_messages(service)

            if messages:
                for msg in messages:
                    msg_id = msg['id']

                    if msg_id in processed_ids:
                        continue

                    msg_id, sender, subject, snippet, date = get_message_details(service, msg_id)

                    task_file = create_task_from_email(msg_id, sender, subject, snippet, date)

                    if task_file:
                        processed_ids.add(msg_id)
                        save_processed_id(msg_id)
                        log_event(f"GMAIL_TRIGGERED - {task_file.name}")
                        trigger_claude_scheduler()

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log_event("GMAIL WATCHER STOPPED - User interrupt")
            break
        except Exception as e:
            log_event(f"GMAIL_ERROR - {str(e)}")
            time.sleep(10)


if __name__ == "__main__":
    watch_gmail()
