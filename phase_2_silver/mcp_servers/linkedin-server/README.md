# LinkedIn Server (MCP)

## Purpose
MCP server that provides LinkedIn posting and monitoring capabilities with approval validation.

## Type
**MCP Server** - Social media integration

## Risk Level
**Medium** - Posts to public social media platform

## Implementation
**Location**: `../../../mcp_servers/linkedin_server.py`

## Capabilities

### Tools Provided

**post_to_linkedin**
- Posts content to LinkedIn feed
- Requires approved plan
- Validates approval status
- Logs all posts with URLs
- Returns post URL and engagement metrics

**Parameters**:
```json
{
  "content": "Post content text (max 3000 chars)",
  "hashtags": ["#BusinessGrowth", "#AI"],
  "visibility": "public",  // or "connections"
  "media": "path/to/image.jpg"  // optional
}
```

**Response**:
```json
{
  "status": "success",
  "post_url": "https://linkedin.com/posts/...",
  "post_id": "xyz789",
  "posted_at": "2026-02-16T14:20:35Z"
}
```

**read_notifications**
- Reads LinkedIn notifications
- Returns unread notifications
- No approval required (read-only)

**Parameters**:
```json
{
  "limit": 10,
  "unread_only": true
}
```

**Response**:
```json
{
  "status": "success",
  "notifications": [
    {
      "type": "connection_request",
      "from": "John Doe",
      "timestamp": "2026-02-16T10:30:00Z",
      "message": "I'd like to connect..."
    }
  ]
}
```

## Approval Workflow Integration

### Pre-Post Validation

Before posting to LinkedIn, the server:

1. **Checks for approved post draft** in `/Needs_Action` or `/Plans`
2. **Validates approval status**: Must be "Approved"
3. **Verifies content matches** approved draft
4. **Checks posting limits**: Max 3 posts per day
5. **Validates hashtags**: Max 5 hashtags per post

### Post Draft Format

```markdown
# LinkedIn Post Draft

**Goal**: Generate sales leads for [Product/Service]
**Target Audience**: [Industry professionals]

## Post Content
[Your post text here - max 3000 characters]

## Hashtags
#BusinessGrowth #DigitalTransformation #AI

**Risk Level**: Medium
**Approval Required**: Yes
**Approval Status**: Approved

---
Created: 2026-02-16 14:15:30
```

## Configuration

### LinkedIn Credentials

```bash
# .env file
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

### Posting Limits

```python
MAX_POSTS_PER_DAY = 3
MAX_HASHTAGS = 5
MAX_CONTENT_LENGTH = 3000
POSTING_COOLDOWN = 3600  # 1 hour between posts
```

## Logging

All LinkedIn operations logged to:
- `logs/linkedin_actions.log` - Detailed operation log
- `linkedin_posts.json` - Persistent record of posts

**Log Format**:
```
[2026-02-16 14:20:30] [LINKEDIN_SERVER] ACTION - Validating approval for post
[2026-02-16 14:20:31] [LINKEDIN_SERVER] ACTION - Approval validated
[2026-02-16 14:20:35] [LINKEDIN_SERVER] ACTION - Post published: https://linkedin.com/posts/...
[2026-02-16 14:20:36] [LINKEDIN_SERVER] ACTION - Post ID: xyz789
```

## Post Tracking

```json
{
  "post_id": "xyz789",
  "post_url": "https://linkedin.com/posts/...",
  "timestamp": "2026-02-16T14:20:35Z",
  "content": "Post content...",
  "hashtags": ["#BusinessGrowth", "#AI"],
  "plan_id": "20260216-141530-PostPlan",
  "approved_by": "user@company.com",
  "engagement": {
    "likes": 0,
    "comments": 0,
    "shares": 0
  }
}
```

## Error Handling

### Common Errors

**Authentication Failed**
```json
{
  "status": "error",
  "error_type": "authentication",
  "message": "LinkedIn authentication failed - session expired"
}
```

**Rate Limit Exceeded**
```json
{
  "status": "error",
  "error_type": "rate_limit",
  "message": "Daily posting limit reached (3 posts/day)"
}
```

**Content Policy Violation**
```json
{
  "status": "error",
  "error_type": "validation",
  "message": "Content violates LinkedIn policies"
}
```

## Security Features

- **Approval Required**: No post without approved draft
- **Credential Protection**: Credentials in .env (gitignored)
- **Audit Trail**: All posts logged with plan reference
- **Rate Limiting**: Prevents spam (3 posts/day max)
- **Content Validation**: Checks length and format
- **Session Management**: Secure session handling

## Usage Example

### From Claude Desktop

```
User: Post about our new AI service on LinkedIn

Claude: I'll create a LinkedIn post draft for your approval...

[Creates post draft in /Needs_Action with Risk: Medium]

Claude: I've created a post draft. Please review and approve it in:
AI_Employee_Vault/Needs_Action/linkedin-post-draft-20260216-141530.md

[User reviews and adds "Approval Status: Approved"]

Claude: Thank you for approving. Publishing to LinkedIn now...

[Calls linkedin-server MCP]

Claude: ✓ Post published successfully!
View at: https://linkedin.com/posts/...
```

## Best Practices

### Content Guidelines

**Do**:
- Keep posts under 1300 characters for max engagement
- Use 3-5 relevant hashtags
- Include a call-to-action
- Post during business hours (9am-5pm)
- Engage with comments promptly

**Don't**:
- Post more than 3 times per day
- Use excessive hashtags (>5)
- Post controversial content
- Spam or use clickbait
- Post outside business context

### Optimal Posting Times

```python
OPTIMAL_TIMES = {
    'Monday': ['09:00', '12:00', '17:00'],
    'Tuesday': ['09:00', '12:00', '17:00'],
    'Wednesday': ['09:00', '12:00', '17:00'],
    'Thursday': ['09:00', '12:00', '17:00'],
    'Friday': ['09:00', '12:00'],
    'Saturday': [],  # Avoid weekends for B2B
    'Sunday': []
}
```

## Testing

### Manual Test

```bash
# 1. Create approved post draft
cat > AI_Employee_Vault/Needs_Action/test_linkedin_post.md << 'EOF'
# LinkedIn Post Draft

**Goal**: Test LinkedIn posting

## Post Content
This is a test post from my Digital FTE system. 🤖

Testing automation capabilities!

#Automation #AI #Testing

**Risk Level**: Medium
**Approval Status**: Approved
EOF

# 2. Run LinkedIn auto-post
python scripts/linkedin_auto_post.py

# 3. Check logs
tail logs/linkedin_actions.log
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\linkedin_server.py"]
    }
  }
}
```

## Dependencies

```
requests>=2.32.5
beautifulsoup4>=4.12.0
selenium>=4.0.0  # For browser automation
```

## Limitations

- No official LinkedIn API for personal accounts
- Session-based authentication (expires periodically)
- Rate limiting: 3 posts/day recommended
- Media uploads require additional handling
- Analytics limited without API access

## Compliance

### LinkedIn Terms of Service

- No automated bulk actions
- Respect rate limits
- No scraping of user data
- No spam or unsolicited messages
- Comply with content policies

### Best Practices

- Always get approval before posting
- Monitor for policy violations
- Respect user privacy
- Maintain professional tone
- Engage authentically

## Future Enhancements

- [ ] LinkedIn API integration (requires approval)
- [ ] Advanced analytics tracking
- [ ] A/B testing for post content
- [ ] Automated response to comments
- [ ] Connection request automation (with approval)
- [ ] Lead scoring and CRM integration
- [ ] Video post support

## References

- Implementation: `../../../mcp_servers/linkedin_server.py`
- Auto-Post Script: `../../../scripts/linkedin_auto_post.py`
- Setup Guide: `../../../scripts/LINKEDIN_SETUP.md`
- MCP Protocol: https://modelcontextprotocol.io
