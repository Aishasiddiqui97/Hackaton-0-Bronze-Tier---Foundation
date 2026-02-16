# Email Server (MCP)

## Purpose
MCP server that provides email sending capabilities with approval validation and logging.

## Type
**MCP Server** - External action executor

## Risk Level
**Medium** - Sends emails to external recipients

## Implementation
**Location**: `../../../mcp_servers/email_server.py`

This MCP server is part of the Silver Tier architecture and integrates with the approval workflow.

## Capabilities

### Tools Provided

**send_email**
- Sends email via SMTP
- Requires approved plan
- Validates approval status
- Logs all sent emails
- Returns message ID and status

**Parameters**:
```json
{
  "to": "recipient@example.com",
  "subject": "Email subject",
  "body": "Email body content",
  "cc": ["cc@example.com"],  // optional
  "bcc": ["bcc@example.com"],  // optional
  "attachments": ["path/to/file.pdf"]  // optional
}
```

**Response**:
```json
{
  "status": "success",
  "message_id": "abc123",
  "sent_at": "2026-02-16T14:20:35Z",
  "recipients": ["recipient@example.com"]
}
```

## Approval Workflow Integration

### Pre-Send Validation

Before sending any email, the server:

1. **Checks for latest plan** in `/Plans` or `/Needs_Action`
2. **Validates approval status**:
   - Low risk: Auto-approved
   - Medium/High risk: Requires "Approval Status: Approved"
3. **Verifies plan fields**:
   - Goal
   - Risk Level
   - Approval Status
4. **Validates recipient** against plan context

### Approval Validation Logic

```python
def validate_approval(plan_path):
    """
    Check if the plan allows for execution based on risk and approval.
    """
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
```

## Configuration

### SMTP Settings

```bash
# .env file
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
```

### Email Defaults

```python
DEFAULT_FROM = "your.email@gmail.com"
DEFAULT_SIGNATURE = "\n\n--\nSent via Digital FTE System"
MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25MB
```

## Logging

All email operations logged to:
- `logs/gmail_actions.log` - Detailed operation log
- `sent_emails.json` - Persistent record of sent emails

**Log Format**:
```
[2026-02-16 14:20:30] [EMAIL_SERVER] ACTION - Validating approval for email send
[2026-02-16 14:20:31] [EMAIL_SERVER] ACTION - Approval validated: Plan 20260216-141530-Plan.md
[2026-02-16 14:20:35] [EMAIL_SERVER] ACTION - Email sent to recipient@example.com
[2026-02-16 14:20:35] [EMAIL_SERVER] ACTION - Message ID: abc123
```

## Sent Email Tracking

```json
{
  "message_id": "abc123",
  "timestamp": "2026-02-16T14:20:35Z",
  "to": ["recipient@example.com"],
  "subject": "Q4 Proposal",
  "plan_id": "20260216-141530-Plan",
  "approved_by": "user@company.com",
  "status": "sent"
}
```

## Error Handling

### Common Errors

**Authentication Failed**
```json
{
  "status": "error",
  "error_type": "authentication",
  "message": "SMTP authentication failed - check credentials"
}
```

**Approval Not Found**
```json
{
  "status": "error",
  "error_type": "approval",
  "message": "No approved plan found for this action"
}
```

**Invalid Recipient**
```json
{
  "status": "error",
  "error_type": "validation",
  "message": "Invalid email address format"
}
```

**Attachment Too Large**
```json
{
  "status": "error",
  "error_type": "validation",
  "message": "Attachment exceeds 25MB limit"
}
```

## Security Features

- **Approval Required**: No email sent without approved plan
- **Credential Protection**: SMTP credentials in .env (gitignored)
- **Audit Trail**: All emails logged with plan reference
- **Rate Limiting**: Prevents spam/abuse
- **Recipient Validation**: Checks email format
- **Content Sanitization**: Prevents injection attacks

## Usage Example

### From Claude Desktop

```
User: Send the Q4 proposal to client@example.com

Claude: I'll help you send that email. First, let me create a plan...

[Creates plan in /Needs_Action with Risk: Medium]

Claude: I've created a plan for sending the email. Please review and approve it in:
AI_Employee_Vault/Needs_Action/20260216-141530-Plan.md

[User reviews and adds "Approval Status: Approved"]

Claude: Thank you for approving. Sending email now...

[Calls email-server MCP]

Claude: ✓ Email sent successfully to client@example.com
Message ID: abc123
```

### From MCP Orchestrator

```python
# Automated execution after approval
mcp_request = {
    "server": "email-server",
    "action": "send_email",
    "parameters": {
        "to": "client@example.com",
        "subject": "Q4 Proposal",
        "body": "Please find attached our Q4 proposal...",
        "attachments": ["docs/Q4_Proposal.pdf"]
    }
}

response = mcp_call(mcp_request)
# Response: {"status": "success", "message_id": "abc123"}
```

## Testing

### Manual Test

```bash
# 1. Create approved plan
cat > AI_Employee_Vault/Plans/test_email_plan.md << 'EOF'
# Plan: Test Email Send

**Goal**: Test email server functionality

**Risk Level**: Medium
**Approval Status**: Approved

## Steps
1. Send test email to test@example.com
EOF

# 2. Test email send via Python
python -c "
from mcp_servers.email_server import send_email
result = send_email('test@example.com', 'Test', 'This is a test')
print(result)
"

# 3. Check logs
tail logs/gmail_actions.log
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "email-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\email_server.py"]
    }
  }
}
```

## Dependencies

```
smtplib (built-in)
email (built-in)
python-dotenv>=1.0.0
```

## Limitations

- SMTP only (no Exchange/Office365 native support)
- 25MB attachment limit (SMTP standard)
- Rate limiting may apply based on SMTP provider
- Requires app-specific password for Gmail

## Future Enhancements

- [ ] HTML email templates
- [ ] Email scheduling
- [ ] Read receipts
- [ ] Email threading
- [ ] Multiple SMTP account support
- [ ] Exchange/Office365 integration
- [ ] Email analytics

## References

- Implementation: `../../../mcp_servers/email_server.py`
- MCP Protocol: https://modelcontextprotocol.io
- Silver Architecture: `../../docs/silver_architecture.md`
