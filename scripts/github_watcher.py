import os
import time
import json
from datetime import datetime
from pathlib import Path
import requests

# Configuration
CHECK_INTERVAL = 60  # seconds - v2.0 Silver Tier
LOG_PATH = "logs/actions.log"
PROCESSED_EVENTS_FILE = "github_processed.json"
INBOX_PATH = Path("AI_Employee_Vault/Inbox")
CONFIG_FILE = Path("AI_Employee_Vault/scripts/github_config.json")

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
INBOX_PATH.mkdir(parents=True, exist_ok=True)


def log_event(event):
    """Log event to actions.log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] {event}\n")
        print(f"[{timestamp}] {event}")
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")


def load_config():
    """Load GitHub configuration from JSON file."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            log_event("ERROR - github_config.json not found")
            return None
    except Exception as e:
        log_event(f"ERROR - Failed to load config: {e}")
        return None


def load_processed_events():
    """Load set of already processed event IDs from JSON."""
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


def show_notification(title, message, event_type):
    """Show Windows toast notification."""
    try:
        # Map event types to icons
        icon_map = {
            "IssuesEvent": "🐛",
            "PullRequestEvent": "🔀",
            "PushEvent": "📤",
            "CreateEvent": "🎉"
        }

        icon = icon_map.get(event_type, "📢")
        full_title = f"{icon} {title}"

        # Use PowerShell for Windows toast notification
        ps_script = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">{full_title}</text>
            <text id="2">{message}</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("GitHub Watcher")
$notifier.Show($toast)
'''

        import subprocess
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            timeout=5
        )

        log_event(f"NOTIFICATION_SHOWN - {title}")
        return True

    except Exception as e:
        log_event(f"NOTIFICATION_FAILED - {e}")
        return False


def save_processed_event(event_id):
    """Save processed event ID to file."""
    with open(PROCESSED_EVENTS_FILE, "a") as f:
        f.write(f"{event_id}\n")


def get_github_events(config):
    """Fetch recent events from GitHub repository."""
    try:
        repo = config.get("repository")
        token = config.get("github_token")

        if not repo or not token:
            log_event("ERROR - Repository or token not configured")
            return []

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get repository events
        url = f"https://api.github.com/repos/{repo}/events"
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            log_event("ERROR - GitHub authentication failed. Check your token.")
            return []
        elif response.status_code == 404:
            log_event(f"ERROR - Repository '{repo}' not found")
            return []
        else:
            log_event(f"ERROR - GitHub API returned status {response.status_code}")
            return []

    except requests.exceptions.Timeout:
        log_event("ERROR - GitHub API request timed out")
        return []
    except Exception as e:
        log_event(f"ERROR - Failed to fetch GitHub events: {e}")
        return []


def filter_event(event, config):
    """Check if event should be processed based on configuration."""
    event_type = event.get("type")
    monitored_events = config.get("monitored_events", [])

    # Map GitHub event types to our configuration
    event_map = {
        "IssuesEvent": "issues",
        "PullRequestEvent": "pull_requests",
        "PushEvent": "pushes",
        "CreateEvent": "repository_creation"
    }

    config_key = event_map.get(event_type)

    if config_key and config_key in monitored_events:
        # For CreateEvent, only process repository creation (not branches/tags)
        if event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            return ref_type == "repository"
        return True

    return False


def create_task_from_event(event, config):
    """Create a task file from GitHub event - v2.0 Silver Tier format."""
    try:
        INBOX_PATH.mkdir(parents=True, exist_ok=True)

        event_type = event.get("type")
        event_id = event.get("id")
        created_at = event.get("created_at", "Unknown")
        actor = event.get("actor", {}).get("login", "Unknown")
        repo = event.get("repo", {}).get("name", "Unknown")

        # Extract event-specific details
        payload = event.get("payload", {})

        # Determine content and risk level based on event type
        content = ""
        risk_level = "Low"

        if event_type == "IssuesEvent":
            action = payload.get("action", "unknown")
            issue = payload.get("issue", {})
            title = issue.get("title", "No title")
            number = issue.get("number", "?")
            content = f"Issue #{number} {action}: {title}"
            risk_level = "Medium"

        elif event_type == "PullRequestEvent":
            action = payload.get("action", "unknown")
            pr = payload.get("pull_request", {})
            title = pr.get("title", "No title")
            number = pr.get("number", "?")
            content = f"Pull Request #{number} {action}: {title}"
            risk_level = "Medium"

        elif event_type == "PushEvent":
            ref = payload.get("ref", "unknown").replace("refs/heads/", "")
            commits = payload.get("commits", [])
            commit_count = len(commits)
            content = f"Pushed {commit_count} commit(s) to {ref}"
            risk_level = "Low"

        elif event_type == "CreateEvent":
            ref_type = payload.get("ref_type", "unknown")
            ref = payload.get("ref", "")
            if ref_type == "repository":
                content = f"Created new repository: {repo}"
                risk_level = "Medium"
            else:
                content = f"Created {ref_type}: {ref}"
                risk_level = "Low"
        else:
            content = f"{event_type} in {repo}"
            risk_level = "Low"

        # v2.0 Silver Tier format
        task_content = f"""# GitHub Event

Type: {event_type}
User: {actor}
Content: {content}
Timestamp: {created_at}
Risk Level: {risk_level}
"""

        # Create filename with event ID
        filename = f"github-{event_id}.md"
        task_file = INBOX_PATH / filename

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)

        log_event(f"GITHUB_NEW - {event_type} by {actor}")
        return task_file

    except Exception as e:
        log_event(f"GITHUB_ERROR - Failed to create task file: {e}")
        return None


def watch_github():
    """Main GitHub watching loop - v2.0 Silver Tier."""
    log_event("GITHUB WATCHER STARTED - v2.0 Silver Tier")

    config = load_config()
    if not config:
        log_event("GITHUB_ERROR - Failed to load configuration")
        return

    repo = config.get("repository", "Not configured")
    log_event(f"Monitoring repository: {repo}")
    log_event(f"Monitored events: {', '.join(config.get('monitored_events', []))}")

    processed_events = load_processed_events()
    log_event(f"Loaded {len(processed_events)} previously processed event IDs")

    while True:
        try:
            events = get_github_events(config)

            if events:
                log_event(f"Found {len(events)} recent event(s)")

                for event in events:
                    event_id = event.get("id")

                    # Skip if already processed
                    if event_id in processed_events:
                        continue

                    event_type = event.get("type")

                    # Check if we should process this event type
                    if not filter_event(event, config):
                        processed_events.add(event_id)
                        save_processed_event(event_id)
                        continue

                    # Create task file
                    task_file = create_task_from_event(event, config)

                    if task_file:
                        # Mark as processed
                        processed_events.add(event_id)
                        save_processed_event(event_id)

                        log_event(f"GITHUB_TRIGGERED - {task_file.name}")
                    else:
                        actor = event.get("actor", {}).get("login", "Unknown")
                        log_event(f"GITHUB_ERROR - Failed to create task for {event_type} by {actor}")

            # Wait before next check
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log_event("GITHUB WATCHER STOPPED - User interrupt")
            break

        except Exception as e:
            log_event(f"GITHUB_ERROR - {str(e)}")
            time.sleep(10)


if __name__ == "__main__":
    watch_github()
