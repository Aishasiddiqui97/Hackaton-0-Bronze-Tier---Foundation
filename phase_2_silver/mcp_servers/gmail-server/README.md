# Gmail Server (MCP)

## Purpose
MCP server that provides Gmail reading and search capabilities via Google Gmail API.

## Type
**MCP Server** - Email integration (read-only)

## Risk Level
**Low** - Read-only operations, no email sending

## Implementation
**Location**: `../../../mcp_servers/gmail_server.py`

## Capabilities

### Tools Provided

**read_emails**
- Reads emails from Gmail inbox
- Supports filtering by sender, subject, date
- Returns email metadata and content
- No approval required (read-only)

**Parameters**:
```json
{
  "query": "from:client@example.com subject:proposal",
  "max_results": 10,
  "include_body": true,
  "mark_as_read": false
}
```

**Response**:
```json
{
  "status": "success",
  "emails": [
    {
      "id": "abc123",
      "from": "client@example.com",
      "subject": "Q4 Proposal Request",
      "date": "2026-02-16T10:30:00Z",
      "body": "Email content...",
      "labels": ["INBOX", "UNREAD"]
    }
  ],
  "count": 1
}
```

**search_emails**
- Advanced email search using Gmail query syntax
- Supports complex queries
- Returns matching email IDs and metadata

**Parameters**:
```json
{
  "query": "is:unread after:2026/02/15",
  "max_results": 50
}
```

**get_email_by_id**
- Retrieves specific email by message ID
- Returns full email details including attachments

**Parameters**:
```json
{
  "message_id": "abc123",
  "include_attachments": false
}
```

## Configuration

### Gmail API Setup

```bash
# Required files
credentials.json  # OAuth credentials from Google Cloud Console
token.json       # Generated OAuth token (auto-created)
```

### Environment Variables

```bash
GMAIL_CHECK_INTERVAL=60  # Seconds between checks
GMAIL_MAX_RESULTS=100    # Max emails per query
```

## Gmail API Authentication

### Setup Steps

1. **Enable Gmail API**
   - Go to https://console.cloud.google.com/
   - Create project or select existing
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json`

2. **First Run Authentication**
   ```bash
   python mcp_servers/gmail_server.py
   ```
   - Browser opens for OAuth consent
   - Grant permissions
   - `token.json` created automatically

3. **Token Refresh**
   - Token auto-refreshes when expired
   - Manual refresh if needed: delete `token.json` and re-authenticate

## Query Syntax

### Gmail Search Operators

```
from:sender@example.com          # From specific sender
to:recipient@example.com         # To specific recipient
subject:keyword                  # Subject contains keyword
has:attachment                   # Has attachments
is:unread                        # Unread emails
is:starred                       # Starred emails
after:2026/02/15                 # After specific date
before:2026/02/20                # Before specific date
newer_than:7d                    # Newer than 7 days
older_than:30d                   # Older than 30 days
label:important                  # Has specific label
```

### Complex Queries

```python
# Unread emails from client in last 7 days
query = "from:client@example.com is:unread newer_than:7d"

# Emails with attachments about proposals
query = "subject:proposal has:attachment"

# Important emails not yet read
query = "is:important is:unread"
```

## Integration with Silver Tier

### Use Cases

**Email Monitoring**
- Gmail Watcher uses this server to poll for new emails
- Converts emails to tasks in Inbox
- Triggers reasoning engine for plan generation

**Email Context Retrieval**
- When responding to emails, retrieve original message
- Get conversation thread context
- Search for related previous emails

**Email Analysis**
- Analyze email patterns
- Identify important senders
- Track response times

## Logging

All Gmail operations logged to:
- `logs/gmail_actions.log` - Detailed operation log

**Log Format**:
```
[2026-02-16 10:30:45] [GMAIL_SERVER] ACTION - Reading emails with query: is:unread
[2026-02-16 10:30:46] [GMAIL_SERVER] ACTION - Found 5 unread emails
[2026-02-16 10:30:47] [GMAIL_SERVER] ACTION - Email IDs: [abc123, def456, ...]
```

## Error Handling

### Common Errors

**Authentication Failed**
```json
{
  "status": "error",
  "error_type": "authentication",
  "message": "OAuth token expired or invalid"
}
```

**API Quota Exceeded**
```json
{
  "status": "error",
  "error_type": "quota",
  "message": "Gmail API quota exceeded - retry after cooldown"
}
```

**Invalid Query**
```json
{
  "status": "error",
  "error_type": "validation",
  "message": "Invalid Gmail query syntax"
}
```

## Security Features

- **Read-Only**: Cannot send or delete emails
- **OAuth 2.0**: Secure authentication
- **Token Storage**: Local token.json (gitignored)
- **Audit Trail**: All reads logged
- **Quota Management**: Respects API limits

## API Quotas

### Gmail API Limits

- **Quota**: 250 quota units per user per second
- **Daily Limit**: 1 billion quota units per day
- **Per Request**:
  - Read email: 5 units
  - Search: 5 units
  - List: 5 units

### Quota Management

```python
# Rate limiting
REQUESTS_PER_SECOND = 10  # Well under 250 quota units/sec
COOLDOWN_ON_ERROR = 60    # Wait 60s if quota exceeded

# Exponential backoff
def read_with_backoff(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return read_emails(query)
        except QuotaExceeded:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    raise QuotaExceeded("Max retries exceeded")
```

## Usage Example

### From Claude Desktop

```
User: Check my unread emails from clients

Claude: Let me check your Gmail for unread emails from clients...

[Calls gmail-server MCP]

Claude: You have 3 unread emails from clients:

1. From: client@example.com
   Subject: Q4 Proposal Request
   Date: Feb 16, 10:30 AM

2. From: partner@company.com
   Subject: Meeting Follow-up
   Date: Feb 16, 9:15 AM

3. From: prospect@startup.com
   Subject: Demo Request
   Date: Feb 15, 4:30 PM

Would you like me to create tasks for any of these?
```

### From Python

```python
from mcp_servers.gmail_server import read_emails

# Read unread emails
result = read_emails(
    query="is:unread",
    max_results=10,
    include_body=True
)

for email in result['emails']:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Date: {email['date']}")
    print("---")
```

## Testing

### Manual Test

```bash
# Test authentication
python mcp_servers/gmail_server.py --test-auth

# Test email reading
python -c "
from mcp_servers.gmail_server import read_emails
result = read_emails('is:unread', max_results=5)
print(f'Found {result[\"count\"]} unread emails')
"

# Check logs
tail logs/gmail_actions.log
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\gmail_server.py"]
    }
  }
}
```

## Dependencies

```
google-auth>=2.27.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.116.0
```

## Limitations

- Read-only (cannot send, delete, or modify emails)
- Requires OAuth consent (one-time setup)
- Subject to Gmail API quotas
- Attachment handling requires additional processing
- No real-time push notifications (polling only)

## Privacy & Security

- **Local Storage**: All data stored locally
- **No Cloud Sync**: Emails not sent to external services
- **OAuth Scopes**: Minimal required permissions
- **Token Security**: Token.json gitignored
- **Audit Trail**: All access logged

## Future Enhancements

- [ ] Real-time push notifications via Pub/Sub
- [ ] Attachment download and processing
- [ ] Email threading and conversation tracking
- [ ] Smart categorization (work vs personal)
- [ ] Integration with calendar for meeting emails
- [ ] Email analytics and insights

## References

- Implementation: `../../../mcp_servers/gmail_server.py`
- Gmail Watcher: `../../../scripts/gmail_watcher.py`
- Setup Guide: `../../../scripts/GMAIL_SETUP.md`
- Gmail API: https://developers.google.com/gmail/api
- MCP Protocol: https://modelcontextprotocol.io
