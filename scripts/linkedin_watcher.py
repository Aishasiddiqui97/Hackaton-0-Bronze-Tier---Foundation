import os
import time
import json
from datetime import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import re

# Configuration
CHECK_INTERVAL = 60  # seconds
LOG_PATH = "logs/linkedin_actions.log"
PROCESSED_EVENTS_FILE = "linkedin_processed.json"
INBOX_PATH = Path("AI_Employee_Vault/Inbox")
TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
INBOX_PATH.mkdir(parents=True, exist_ok=True)


def log_event(event):
    """Log event to linkedin_actions.log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] [LINKEDIN_WATCHER] ACTION - {event}"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")


def load_processed_events():
    """Load set of already processed LinkedIn event IDs from JSON."""
    if os.path.exists(PROCESSED_EVENTS_FILE):
        try:
            with open(PROCESSED_EVENTS_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("processed_ids", []))
        except (json.JSONDecodeError, FileNotFoundError):
            return set()
    return set()


def save_processed_event(event_id):
    """Save processed event ID to JSON file."""
    processed = load_processed_events()
    processed.add(event_id)

    with open(PROCESSED_EVENTS_FILE, "w") as f:
        json.dump({"processed_ids": list(processed)}, f, indent=2)


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def is_spam_linkedin_email(subject, snippet):
    """Filter out promotional/spam LinkedIn emails."""
    spam_keywords = [
        "discover opportunities",
        "grow your career",
        "jobs you may be interested",
        "people you may know",
        "trending posts",
        "weekly digest",
        "news from your network",
        "see who's hiring",
        "recommended for you",
        "top posts",
        "daily rundown"
    ]

    subject_lower = subject.lower()
    snippet_lower = snippet.lower()

    for keyword in spam_keywords:
        if keyword in subject_lower or keyword in snippet_lower:
            return True

    return False


def parse_linkedin_event(subject, snippet):
    """Parse LinkedIn email to determine event type and extract details."""
    subject_lower = subject.lower()
    
    # Connection requests
    if "wants to connect" in subject_lower or "invitation to connect" in subject_lower:
        name_match = re.search(r'^(.+?)\s+(?:wants to connect|invited you|sent you)', subject, re.IGNORECASE)
        name = name_match.group(1) if name_match else "Someone"
        return {
            "type": "Connection Request",
            "name": name,
            "details": f"{name} wants to connect with you on LinkedIn",
            "risk": "Low"
        }

    # Messages
    elif "sent you a message" in subject_lower or "new message" in subject_lower:
        name_match = re.search(r'^(.+?)\s+sent you', subject, re.IGNORECASE)
        name = name_match.group(1) if name_match else "Someone"
        return {
            "type": "Message",
            "name": name,
            "details": snippet,
            "risk": "Medium"
        }

    # Generic Notification
    else:
        return {
            "type": "Notification",
            "name": "LinkedIn",
            "details": f"{subject}: {snippet}",
            "risk": "Low"
        }


def create_task_from_linkedin_event(event_data, message_id, date):
    """Create a task file from LinkedIn event using v2.0 Silver Tier format."""
    try:
        INBOX_PATH.mkdir(parents=True, exist_ok=True)

        event_type = event_data["type"]
        name = event_data["name"]
        details = event_data["details"]
        risk_level = event_data["risk"]

        task_content = f"""# LinkedIn Event

Type: {event_type}
User: {name}
Content: {details}
Timestamp: {date}
Risk Level: {risk_level}
"""

        filename = f"linkedin-{message_id}.md"
        task_file = INBOX_PATH / filename

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)

        log_event(f"LINKEDIN_NEW - {event_type} from {name}")
        return task_file

    except Exception as e:
        log_event(f"LINKEDIN_ERROR - Failed to create task file: {e}")
        return None

def trigger_claude_scheduler():
    """Trigger the Reasoning Engine via Claude Scheduler."""
    try:
        log_event("Executing: claude scheduler --once")
        import subprocess
        result = subprocess.run(["claude", "scheduler", "--once"], capture_output=True, text=True, shell=True)
        return True
    except Exception as e:
        log_event(f"Trigger failed: {e}")
        return False


def watch_linkedin():
    """Main LinkedIn watching loop - v2.0 Silver Tier."""
    log_event("LINKEDIN WATCHER STARTED - v2.0 Silver Tier")

    try:
        service = get_gmail_service()
        log_event("Gmail API authenticated successfully for LinkedIn sensor")
    except Exception as e:
        log_event(f"LINKEDIN_ERROR - Failed to authenticate: {e}")
        return

    processed_events = load_processed_events()
    log_event(f"Loaded {len(processed_events)} previously processed LinkedIn event IDs")

    while True:
        try:
            # Search for LinkedIn emails (Unread only)
            query = "from:linkedin.com is:unread"
            results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
            messages = results.get('messages', [])

            if messages:
                for msg in messages:
                    msg_id = msg['id']

                    if msg_id in processed_events:
                        continue

                    try:
                        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                        headers = message['payload']['headers']
                        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown')
                        snippet = message.get('snippet', '')

                        if is_spam_linkedin_email(subject, snippet):
                            processed_events.add(msg_id)
                            save_processed_event(msg_id)
                            continue

                        event_data = parse_linkedin_event(subject, snippet)
                        task_file = create_task_from_linkedin_event(event_data, msg_id, date)

                        if task_file:
                            processed_events.add(msg_id)
                            save_processed_event(msg_id)
                            log_event(f"LINKEDIN_TRIGGERED - {task_file.name}")
                            trigger_claude_scheduler()

                    except Exception as e:
                        log_event(f"LINKEDIN_ERROR - Failed to process message {msg_id}: {e}")
                        processed_events.add(msg_id)
                        save_processed_event(msg_id)
                        continue

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log_event("LINKEDIN WATCHER STOPPED - User interrupt")
            break
        except Exception as e:
            log_event(f"LINKEDIN_ERROR - Watch loop error: {str(e)}")
            time.sleep(10)


if __name__ == "__main__":
    watch_linkedin()
