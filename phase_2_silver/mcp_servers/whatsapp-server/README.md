# WhatsApp Server (MCP)

## Purpose
MCP server that provides WhatsApp message reading capabilities.

## Type
**MCP Server** - Messaging integration (read-only)

## Risk Level
**Low** - Read-only operations, no message sending

## Implementation
**Location**: `../../../mcp_servers/whatsapp_server.py`

## Capabilities

### Tools Provided

**read_messages**
- Reads WhatsApp messages
- Supports filtering by contact, date
- Returns message metadata and content
- No approval required (read-only)

**Parameters**:
```json
{
  "contact": "Client Name",
  "unread_only": true,
  "max_results": 10,
  "since": "2026-02-15T00:00:00Z"
}
```

**Response**:
```json
{
  "status": "success",
  "messages": [
    {
      "id": "whatsapp-123456",
      "from": "Client Name",
      "content": "Can you send the proposal?",
      "timestamp": "2026-02-16T10:30:00Z",
      "type": "text",
      "unread": true
    }
  ],
  "count": 1
}
```

**get_contacts**
- Retrieves list of WhatsApp contacts
- Returns contact names and numbers
- Useful for filtering and routing

**Parameters**:
```json
{
  "business_only": true
}
```

**Response**:
```json
{
  "status": "success",
  "contacts": [
    {
      "name": "Client Name",
      "number": "+1234567890",
      "type": "business"
    }
  ]
}
```

## Configuration

### WhatsApp Web Session

```bash
# Session management
WHATSAPP_SESSION_FILE=whatsapp_session.json
WHATSAPP_CHECK_INTERVAL=90  # Seconds between checks
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

## WhatsApp Web Authentication

### Setup Steps

1. **Initial Authentication**
   ```bash
   python mcp_servers/whatsapp_server.py --setup
   ```
   - Browser opens WhatsApp Web
   - Scan QR code with phone
   - Session saved to `whatsapp_session.json`

2. **Session Persistence**
   - Session valid for ~14 days
   - Auto-refresh if still active
   - Re-scan QR if expired

3. **Multi-Device Support**
   - WhatsApp multi-device beta required
   - Allows web session without phone online

## Integration with Silver Tier

### Use Cases

**Message Monitoring**
- WhatsApp Watcher uses this server to poll for new messages
- Converts messages to tasks in Inbox
- Triggers reasoning engine for plan generation

**Message Context Retrieval**
- When responding to messages, retrieve conversation history
- Get context for better responses
- Track communication patterns

**Business Communication**
- Filter business vs personal messages
- Prioritize important contacts
- Route urgent messages appropriately

## Logging

All WhatsApp operations logged to:
- `logs/whatsapp_actions.log` - Detailed operation log

**Log Format**:
```
[2026-02-16 10:30:45] [WHATSAPP_SERVER] ACTION - Reading messages from Client Name
[2026-02-16 10:30:46] [WHATSAPP_SERVER] ACTION - Found 2 unread messages
[2026-02-16 10:30:47] [WHATSAPP_SERVER] ACTION - Messages processed
```

## Error Handling

### Common Errors

**Session Expired**
```json
{
  "status": "error",
  "error_type": "authentication",
  "message": "WhatsApp Web session expired - please re-scan QR code"
}
```

**Rate Limiting**
```json
{
  "status": "error",
  "error_type": "rate_limit",
  "message": "Too many requests - reducing polling frequency"
}
```

**Connection Failed**
```json
{
  "status": "error",
  "error_type": "connection",
  "message": "Cannot connect to WhatsApp Web - check internet connection"
}
```

## Security Features

- **Read-Only**: Cannot send messages
- **Session Encryption**: Session file encrypted
- **Local Storage**: Messages stored locally only
- **Audit Trail**: All reads logged
- **Contact Filtering**: Only monitor approved contacts

## Message Types

### Supported Types

**Text Messages**
- Plain text content
- Emojis supported
- Links extracted

**Media Messages**
- Images (metadata only)
- Videos (metadata only)
- Documents (filename and type)
- Audio (duration)

**System Messages**
- Contact joined WhatsApp
- Group notifications
- Call notifications

### Unsupported Types

- Voice messages (transcription not implemented)
- Stickers (treated as media)
- Live location (not accessible via web)

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

## Usage Example

### From Claude Desktop

```
User: Check my WhatsApp messages from clients

Claude: Let me check your WhatsApp for messages from business contacts...

[Calls whatsapp-server MCP]

Claude: You have 2 unread messages from clients:

1. From: Client Name
   Message: "Can you send the proposal by tomorrow?"
   Time: 10:30 AM

2. From: Business Partner
   Message: "Meeting confirmed for 2pm"
   Time: 9:15 AM

Would you like me to create tasks for these?
```

### From Python

```python
from mcp_servers.whatsapp_server import read_messages

# Read unread messages from business contacts
result = read_messages(
    unread_only=True,
    business_only=True,
    max_results=10
)

for msg in result['messages']:
    print(f"From: {msg['from']}")
    print(f"Message: {msg['content']}")
    print(f"Time: {msg['timestamp']}")
    print("---")
```

## Testing

### Manual Test

```bash
# Test session
python mcp_servers/whatsapp_server.py --test-session

# Test message reading
python -c "
from mcp_servers.whatsapp_server import read_messages
result = read_messages(unread_only=True)
print(f'Found {result[\"count\"]} unread messages')
"

# Check logs
tail logs/whatsapp_actions.log
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "whatsapp-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\whatsapp_server.py"]
    }
  }
}
```

## Dependencies

```
selenium>=4.0.0          # Browser automation
webdriver-manager>=4.0.0 # Chrome driver management
beautifulsoup4>=4.12.0   # HTML parsing
cryptography>=41.0.0     # Session encryption
```

## Limitations

### Technical Limitations

- Requires WhatsApp Web to be active
- Cannot send messages (read-only)
- Media files require manual handling
- Group messages may be noisy
- Session expires after ~14 days

### WhatsApp Restrictions

- No official API for personal accounts
- Web scraping may violate ToS
- Rate limiting applies
- Multi-device beta required for best experience

### Recommended Approach

For production use, consider:
- **WhatsApp Business API** (official, requires approval)
- **Twilio WhatsApp** integration
- **Manual message handling** for sensitive communications

## Alternative Implementations

### Option 1: WhatsApp Business API (Recommended)

**Pros**:
- Official API from Meta
- Reliable and supported
- Better features

**Cons**:
- Requires business verification
- Costs money
- Setup complexity

### Option 2: Twilio WhatsApp

**Pros**:
- Easy setup
- Good documentation
- Pay-per-message

**Cons**:
- Ongoing costs
- Third-party dependency

### Option 3: Manual Monitoring (Current)

**Pros**:
- No API required
- Free
- Works with personal accounts

**Cons**:
- Limited automation
- Requires active session
- May violate ToS

## Future Enhancements

- [ ] WhatsApp Business API integration
- [ ] Media file handling (images, documents)
- [ ] Voice message transcription
- [ ] Automated responses for common queries
- [ ] Integration with CRM systems
- [ ] Multi-device support improvements
- [ ] Message templates

## References

- Implementation: `../../../mcp_servers/whatsapp_server.py`
- WhatsApp Watcher: `../../../scripts/whatsapp_watcher.py`
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- Twilio WhatsApp: https://www.twilio.com/whatsapp
- MCP Protocol: https://modelcontextprotocol.io
