# Gmail Watcher Skill

## Purpose
Monitors Gmail inbox for new emails and converts them into actionable tasks in the Digital FTE system.

## Type
**Input Watcher Skill** - Autonomous monitoring agent

## Risk Level
**Low** - Read-only operation, no external modifications

## Implementation
**Location**: `../../scripts/gmail_watcher.py`

This skill is implemented in the root scripts folder and integrated into Silver Tier architecture.

## Functionality

### What It Does
1. Authenticates with Gmail API using OAuth2
2. Polls inbox every 60 seconds for unread emails
3. Extracts email metadata (sender, subject, body, timestamp)
4. Creates structured task files in `AI_Employee_Vault/Inbox/`
5. Marks emails as read (optional)
6. Logs all operations to `logs/gmail_actions.log`

### Task File Format

```markdown
# Email: [Subject]

**From**: [sender@email.com]
**Received**: [timestamp]
**Priority**: [High/Medium/Low]

## Content
[Email body content]

## Suggested Actions
- [Action 1]
- [Action 2]

---
Source: Gmail
ID: gmail-[message_id]
```

## Configuration

### Required Credentials
- `credentials.json` - Gmail API OAuth credentials
- `token.json` - Generated OAuth token (auto-created on first run)

### Environment Variables
```bash
GMAIL_CHECK_INTERVAL=60  # Seconds between checks
GMAIL_MARK_READ=true     # Mark processed emails as read
```

## Setup Instructions

### 1. Enable Gmail API
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download as `credentials.json`

### 2. First Run
```bash
cd scripts
python gmail_watcher.py
```
- Browser will open for OAuth consent
- Grant permissions
- `token.json` will be created automatically

### 3. Verify Operation
```bash
# Check logs
tail -f ../logs/gmail_actions.log

# Check inbox for new tasks
ls -la ../AI_Employee_Vault/Inbox/
```

## Integration with Silver Tier

### Input to Reasoning Engine
- Gmail Watcher → Creates task in `/Inbox`
- Vault Watcher (Bronze) → Detects new file
- Reasoning Engine → Generates Plan.md
- Approval Manager → Routes based on risk

### Example Flow
```
New email arrives: "Please send Q4 report to client"
    ↓
Gmail Watcher creates: Email_20260216_103045_Q4_Report.md
    ↓
Reasoning Engine analyzes: High risk (external communication)
    ↓
Creates plan in /Needs_Action with Approval Status: Pending
    ↓
Human reviews and approves
    ↓
MCP Email Server sends report
    ↓
Task moved to /Done
```

## Error Handling

### Common Issues

**Authentication Failed**
- Delete `token.json` and re-authenticate
- Verify `credentials.json` is valid
- Check OAuth consent screen is configured

**API Quota Exceeded**
- Gmail API: 250 quota units/user/second
- Reduce polling frequency
- Implement exponential backoff

**Network Errors**
- Automatic retry with 3 attempts
- 60-second delay between retries
- Logged to error log

## Monitoring

### Health Check
```bash
# Check if watcher is running
ps aux | grep gmail_watcher

# Check recent activity
tail -20 logs/gmail_actions.log

# Check processed email count
grep "Email processed" logs/gmail_actions.log | wc -l
```

### Performance Metrics
- Emails processed per day
- Average processing time
- Error rate
- API quota usage

## Maintenance

### Daily
- Verify watcher is running
- Check for authentication errors

### Weekly
- Review processed email count
- Optimize filtering rules if needed

### Monthly
- Rotate OAuth token if needed
- Review and archive old logs

## Customization

### Email Filtering
Edit `gmail_watcher.py` to add filters:

```python
# Only process emails from specific senders
ALLOWED_SENDERS = ['boss@company.com', 'client@example.com']

# Only process emails with specific subjects
SUBJECT_KEYWORDS = ['urgent', 'action required', 'task']

# Skip automated emails
SKIP_SENDERS = ['noreply@', 'no-reply@', 'notifications@']
```

### Priority Detection
```python
def detect_priority(subject, body):
    high_priority = ['urgent', 'asap', 'critical', 'emergency']
    if any(word in subject.lower() for word in high_priority):
        return "High"
    return "Medium"
```

## Dependencies

```
google-auth>=2.27.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.116.0
```

## Logs

**Location**: `logs/gmail_actions.log`

**Format**:
```
[2026-02-16 10:30:45] [GMAIL_WATCHER] ACTION - New email detected: "Project Update"
[2026-02-16 10:30:46] [GMAIL_WATCHER] ACTION - Created task: Email_20260216_103046_Project_Update.md
[2026-02-16 10:30:47] [GMAIL_WATCHER] ACTION - Email marked as read
```

## Testing

### Manual Test
```bash
# Send yourself a test email with subject "Test Task"
# Watch the logs
tail -f logs/gmail_actions.log

# Verify task created
ls -la AI_Employee_Vault/Inbox/ | grep "Test_Task"
```

### Automated Test
```python
# test_gmail_watcher.py
def test_email_to_task_conversion():
    # Mock email data
    email = {
        'subject': 'Test Task',
        'from': 'test@example.com',
        'body': 'Please complete this task'
    }

    # Process email
    task_file = process_email(email)

    # Verify task created
    assert os.path.exists(task_file)
    assert 'Test Task' in open(task_file).read()
```

## Security

- OAuth tokens stored locally, never committed to git
- Email content stored locally only
- No email forwarding or external transmission
- All operations logged for audit

## Future Enhancements

- [ ] Smart categorization (work vs personal)
- [ ] Attachment handling
- [ ] Thread conversation tracking
- [ ] Auto-response for common queries
- [ ] Integration with calendar for meeting requests

## References

- Gmail API: https://developers.google.com/gmail/api
- OAuth 2.0: https://developers.google.com/identity/protocols/oauth2
- Setup Guide: `../../scripts/GMAIL_SETUP.md`
