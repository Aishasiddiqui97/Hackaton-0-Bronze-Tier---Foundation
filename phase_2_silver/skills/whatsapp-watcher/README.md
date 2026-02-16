# WhatsApp Watcher Skill

## Purpose
Monitors WhatsApp messages and converts them into actionable tasks in the Digital FTE system.

## Type
**Input Watcher Skill** - Message monitoring agent

## Risk Level
**Low** - Read-only operation, no message sending

## Implementation
**Location**: `../../scripts/whatsapp_watcher.py`

## Functionality

### What It Does
1. Monitors WhatsApp Web for new messages
2. Polls every 90 seconds for unread conversations
3. Extracts message metadata (sender, content, timestamp)
4. Creates structured task files in `AI_Employee_Vault/Inbox/`
5. Marks messages as read (optional)
6. Logs all operations to `logs/whatsapp_actions.log`

### Task File Format

```markdown
# WhatsApp Message: [Sender Name]

**From**: [Contact Name or Number]
**Received**: [timestamp]
**Priority**: [High/Medium/Low]
**Type**: [Personal | Business | Group]

## Message Content
[Message text]

## Context
[Previous conversation context if relevant]

## Suggested Actions
- Reply to message
- Schedule follow-up
- Create task

---
Source: WhatsApp
ID: whatsapp-[message_id]
```

## Configuration

### Environment Variables
```bash
WHATSAPP_CHECK_INTERVAL=90   # Seconds between checks
WHATSAPP_MARK_READ=false     # Mark processed messages as read
WHATSAPP_BUSINESS_ONLY=true  # Only process business contacts
```

### Contact Filtering
```python
# whatsapp_config.py
BUSINESS_CONTACTS = [
    '+1234567890',
    'Client Name',
    'Business Partner'
]

IGNORE_CONTACTS = [
    'Spam',
    'Marketing',
    'Notifications'
]

PRIORITY_CONTACTS = [
    'Boss',
    'Important Client'
]
```

## Setup Instructions

### 1. WhatsApp Web Authentication

**Method 1: QR Code (Recommended)**
```bash
cd scripts
python whatsapp_watcher.py
```
- Browser opens WhatsApp Web
- Scan QR code with phone
- Session saved for future use

**Method 2: Session File**
```bash
# Use existing session
cp whatsapp_session.json scripts/
python whatsapp_watcher.py --use-session
```

### 2. Configure Contacts
Edit `whatsapp_config.py` to specify which contacts to monitor.

### 3. Verify Operation
```bash
# Check logs
tail -f ../logs/whatsapp_actions.log

# Check inbox for new tasks
ls -la ../AI_Employee_Vault/Inbox/ | grep WhatsApp
```

## Integration with Silver Tier

### Input Flow
```
WhatsApp message arrives
    ↓
WhatsApp Watcher detects message
    ↓
Creates task in /Inbox
    ↓
Reasoning Engine analyzes
    ↓
Generates response plan (if business-related)
    ↓
Routes to /Needs_Action for approval
    ↓
Human approves response
    ↓
MCP WhatsApp Server sends reply
```

### Example Flow
```
Client sends: "Can you send me the proposal by tomorrow?"
    ↓
Watcher creates: WhatsApp_20260216_103045_Client_Request.md
    ↓
Reasoning Engine: High priority, requires action
    ↓
Creates plan: "Send proposal to client"
    ↓
Routes to /Needs_Action (Risk: Medium - external communication)
    ↓
Human reviews proposal and approves
    ↓
Email sent with proposal
    ↓
WhatsApp reply: "Proposal sent via email"
    ↓
Task moved to /Done
```

## Message Classification

### Priority Detection
```python
def detect_priority(message, sender):
    # High priority indicators
    high_priority_keywords = [
        'urgent', 'asap', 'emergency', 'critical',
        'immediately', 'right now', 'deadline'
    ]

    # Priority contacts always high
    if sender in PRIORITY_CONTACTS:
        return "High"

    # Check message content
    if any(word in message.lower() for word in high_priority_keywords):
        return "High"

    # Business contacts medium priority
    if sender in BUSINESS_CONTACTS:
        return "Medium"

    return "Low"
```

### Message Type Detection
```python
def detect_message_type(sender, message):
    # Group messages
    if '@g.us' in sender:
        return "Group"

    # Business contacts
    if sender in BUSINESS_CONTACTS:
        return "Business"

    # Personal messages
    return "Personal"
```

## Error Handling

### Common Issues

**WhatsApp Web Session Expired**
- Re-scan QR code
- Session expires after 14 days of inactivity
- Automatic re-authentication prompt

**Rate Limiting**
- WhatsApp may throttle if too many requests
- Reduce polling frequency
- Implement exponential backoff

**Message Parsing Errors**
- Handle media messages (images, videos, documents)
- Extract text from media captions
- Log unparseable messages for review

## Monitoring

### Health Check
```bash
# Check if watcher is running
ps aux | grep whatsapp_watcher

# Check recent activity
tail -20 logs/whatsapp_actions.log

# Check processed message count
grep "Message processed" logs/whatsapp_actions.log | wc -l
```

### Performance Metrics
- Messages processed per day
- Average response time
- Business vs personal message ratio
- Priority distribution

## Privacy & Security

### Data Handling
- Messages stored locally only
- No cloud backup of message content
- Automatic deletion after 30 days (configurable)
- Sensitive data redacted in logs

### Access Control
- Session file encrypted
- No message forwarding without approval
- All actions logged for audit
- User controls all data retention

### Compliance
- GDPR compliant (data stored locally)
- No third-party data sharing
- User consent required for monitoring
- Right to delete all data

## Limitations

### Technical Limitations
- Requires WhatsApp Web to be active
- Cannot send messages without approval
- Media files require manual handling
- Group messages may be noisy

### WhatsApp Restrictions
- No official API for personal accounts
- Web scraping may violate ToS
- Session expires periodically
- Rate limiting applies

### Recommended Approach
For production use, consider:
- WhatsApp Business API (official, requires approval)
- Twilio WhatsApp integration
- Manual message handling for sensitive communications

## Dependencies

```
selenium>=4.0.0          # Browser automation
webdriver-manager>=4.0.0 # Chrome driver management
beautifulsoup4>=4.12.0   # HTML parsing
```

## Logs

**Location**: `logs/whatsapp_actions.log`

**Format**:
```
[2026-02-16 10:30:45] [WHATSAPP_WATCHER] ACTION - New message from Client: "Can you send proposal?"
[2026-02-16 10:30:46] [WHATSAPP_WATCHER] ACTION - Created task: WhatsApp_20260216_103046_Client.md
[2026-02-16 10:30:47] [WHATSAPP_WATCHER] ACTION - Priority: High, Type: Business
```

## Testing

### Manual Test
```bash
# Send yourself a WhatsApp message
# Watch the logs
tail -f logs/whatsapp_actions.log

# Verify task created
ls -la AI_Employee_Vault/Inbox/ | grep WhatsApp
```

### Automated Test
```python
# test_whatsapp_watcher.py
def test_message_to_task_conversion():
    # Mock message data
    message = {
        'sender': 'Test Contact',
        'content': 'Please complete this task',
        'timestamp': '2026-02-16 10:30:45'
    }

    # Process message
    task_file = process_message(message)

    # Verify task created
    assert os.path.exists(task_file)
    assert 'Test Contact' in open(task_file).read()
```

## Maintenance

### Daily
- Verify watcher is running
- Check for session expiration
- Review high-priority messages

### Weekly
- Clean up old message files
- Review and optimize filters
- Update contact lists

### Monthly
- Rotate session credentials
- Archive old logs
- Review privacy compliance

## Future Enhancements

- [ ] WhatsApp Business API integration
- [ ] Media file handling (images, documents)
- [ ] Voice message transcription
- [ ] Automated responses for common queries
- [ ] Integration with CRM systems
- [ ] Multi-device support

## Alternative Implementations

### Option 1: WhatsApp Business API (Recommended)
- Official API from Meta
- Requires business verification
- Supports automation
- Better reliability

### Option 2: Twilio WhatsApp Integration
- Third-party service
- Easy setup
- Pay-per-message pricing
- Good documentation

### Option 3: Manual Monitoring (Current)
- No API required
- Free
- Limited automation
- Requires active session

## References

- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- Twilio WhatsApp: https://www.twilio.com/whatsapp
- Setup Guide: `../../scripts/whatsapp_watcher.py`
