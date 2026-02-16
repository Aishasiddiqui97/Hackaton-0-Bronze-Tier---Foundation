# LinkedIn Watcher Skill

## Purpose
Monitors LinkedIn for notifications, messages, and engagement opportunities. Automatically posts business updates to generate sales leads.

## Type
**Input/Output Watcher Skill** - Bidirectional monitoring and posting agent

## Risk Level
**Medium** - Read operations are low risk, posting operations require approval

## Implementation
**Location**: `../../scripts/linkedin_watcher.py` and `../../scripts/linkedin_auto_post.py`

## Functionality

### What It Does

#### Monitoring (Read)
1. Authenticates with LinkedIn (session-based)
2. Polls for new notifications every 120 seconds
3. Detects messages, connection requests, post engagements
4. Creates structured task files in `AI_Employee_Vault/Inbox/`
5. Logs all operations to `logs/linkedin_actions.log`

#### Auto-Posting (Write)
1. Reads approved post drafts from `/Needs_Action`
2. Validates approval status
3. Posts to LinkedIn feed
4. Logs post URL and engagement metrics
5. Moves completed post to `/Done`

### Task File Format

```markdown
# LinkedIn Notification: [Type]

**Type**: [Message | Connection Request | Post Engagement | Comment]
**From**: [User Name]
**Received**: [timestamp]
**Priority**: Medium

## Content
[Notification content]

## Suggested Actions
- Reply to message
- Accept connection request
- Engage with post

---
Source: LinkedIn
ID: linkedin-[notification_id]
```

### Post Draft Format

```markdown
# LinkedIn Post Draft

**Goal**: Generate sales leads for [Product/Service]
**Target Audience**: [Industry professionals / Decision makers / etc.]
**Tone**: [Professional | Casual | Thought Leadership]

## Post Content
[Your post text here - max 3000 characters]

## Hashtags
#BusinessGrowth #DigitalTransformation #AI

## Risk Level**: Medium
**Approval Required**: Yes
**Approval Status**: Pending

---
Created: [timestamp]
```

## Configuration

### Required Credentials
```bash
# .env file
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

### Environment Variables
```bash
LINKEDIN_CHECK_INTERVAL=120  # Seconds between checks
LINKEDIN_AUTO_POST=false     # Enable auto-posting (requires approval)
LINKEDIN_MAX_POSTS_PER_DAY=3 # Rate limiting
```

## Setup Instructions

### 1. Configure Credentials
```bash
# Add to .env file
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_secure_password
```

### 2. Start Watcher
```bash
cd scripts
python linkedin_watcher.py
```

### 3. Test Auto-Posting
```bash
# Create a post draft in Needs_Action
# Add "Approval Status: Approved"
# Run auto-post script
python linkedin_auto_post.py
```

## Integration with Silver Tier

### Input Flow (Monitoring)
```
LinkedIn notification arrives
    ↓
LinkedIn Watcher detects notification
    ↓
Creates task in /Inbox
    ↓
Reasoning Engine analyzes
    ↓
Generates response plan (if needed)
```

### Output Flow (Posting)
```
Business update needed
    ↓
Reasoning Engine creates post draft
    ↓
Saved to /Needs_Action (Risk: Medium)
    ↓
Human reviews and approves
    ↓
LinkedIn Auto-Post publishes
    ↓
Post URL logged, moved to /Done
```

## Risk Assessment

### Low Risk Operations (Auto-approved)
- Reading notifications
- Viewing profiles
- Monitoring engagement metrics

### Medium Risk Operations (Require approval)
- Posting to feed
- Sending messages
- Accepting connection requests
- Commenting on posts

### High Risk Operations (Require explicit approval)
- Posting about sensitive topics
- Bulk messaging
- Automated connection requests

## Error Handling

### Common Issues

**Authentication Failed**
- LinkedIn may require CAPTCHA
- Use session cookies instead of password
- Consider LinkedIn API (requires approval)

**Rate Limiting**
- LinkedIn limits: ~100 requests/hour
- Implement exponential backoff
- Reduce polling frequency

**Post Rejected**
- LinkedIn content policy violation
- Review post content
- Adjust tone or remove flagged content

## Monitoring

### Health Check
```bash
# Check if watcher is running
ps aux | grep linkedin_watcher

# Check recent activity
tail -20 logs/linkedin_actions.log

# Check pending posts
ls -la AI_Employee_Vault/Needs_Action/ | grep linkedin
```

### Performance Metrics
- Notifications processed per day
- Posts published per week
- Engagement rate (likes, comments, shares)
- Connection growth rate

## Auto-Posting Strategy

### Content Types

**Thought Leadership**
- Industry insights
- Trend analysis
- Expert opinions
- Risk: Medium

**Company Updates**
- Product launches
- Team achievements
- Case studies
- Risk: Low-Medium

**Sales Content**
- Service offerings
- Client testimonials
- Special promotions
- Risk: Medium

### Posting Schedule

```python
OPTIMAL_POSTING_TIMES = {
    'Monday': ['09:00', '12:00', '17:00'],
    'Tuesday': ['09:00', '12:00', '17:00'],
    'Wednesday': ['09:00', '12:00', '17:00'],
    'Thursday': ['09:00', '12:00', '17:00'],
    'Friday': ['09:00', '12:00'],
    'Saturday': [],  # Avoid weekends for B2B
    'Sunday': []
}
```

### Content Guidelines

**Best Practices**
- Keep posts under 1300 characters for max engagement
- Use 3-5 relevant hashtags
- Include a call-to-action
- Add visual content when possible
- Tag relevant people/companies (with permission)

**Avoid**
- Excessive self-promotion
- Controversial topics
- Spam or clickbait
- Posting too frequently (max 3/day)

## Sales Lead Generation

### Strategy

1. **Value-First Content**
   - Share helpful insights
   - Solve common problems
   - Demonstrate expertise

2. **Engagement Triggers**
   - Ask questions
   - Request opinions
   - Share polls
   - Encourage discussion

3. **Lead Capture**
   - Monitor comments for interested prospects
   - Create tasks for follow-up
   - Track engagement in CRM

### Example Post Template

```markdown
🚀 [Attention-grabbing headline]

[Problem statement that resonates with target audience]

[Your unique solution or insight]

[Social proof or results]

[Call-to-action]

What's your experience with [topic]? Share in comments 👇

#Hashtag1 #Hashtag2 #Hashtag3
```

## Dependencies

```
requests>=2.32.5
beautifulsoup4>=4.12.0  # For web scraping if needed
selenium>=4.0.0         # For browser automation (alternative)
```

## Logs

**Location**: `logs/linkedin_actions.log`

**Format**:
```
[2026-02-16 10:30:45] [LINKEDIN_WATCHER] ACTION - New notification: Connection request from John Doe
[2026-02-16 10:30:46] [LINKEDIN_WATCHER] ACTION - Created task: LinkedIn_Notification_20260216_103046.md
[2026-02-16 14:15:30] [LINKEDIN_AUTO_POST] ACTION - Post approved: "Digital Transformation Insights"
[2026-02-16 14:15:35] [LINKEDIN_AUTO_POST] ACTION - Post published: https://linkedin.com/posts/...
[2026-02-16 14:15:36] [LINKEDIN_AUTO_POST] ACTION - Moved to Done
```

## Testing

### Test Notification Detection
```bash
# Send yourself a LinkedIn message
# Watch the logs
tail -f logs/linkedin_actions.log

# Verify task created
ls -la AI_Employee_Vault/Inbox/ | grep LinkedIn
```

### Test Auto-Posting
```bash
# Create test post draft
cat > AI_Employee_Vault/Needs_Action/test_post.md << 'EOF'
# LinkedIn Post Draft

**Goal**: Test auto-posting functionality

## Post Content
This is a test post from my Digital FTE system. 🤖

Testing automation capabilities!

#Automation #AI #Testing

**Risk Level**: Medium
**Approval Required**: Yes
**Approval Status**: Approved
EOF

# Run auto-post
python scripts/linkedin_auto_post.py

# Check logs for success
tail logs/linkedin_actions.log
```

## Security

- Credentials stored in `.env` (gitignored)
- Session tokens expire after 24 hours
- No credential logging
- Rate limiting prevents account suspension
- All posts require human approval

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

## Future Enhancements

- [ ] LinkedIn API integration (requires approval)
- [ ] Advanced analytics tracking
- [ ] A/B testing for post content
- [ ] Automated response to common messages
- [ ] Connection request automation (with approval)
- [ ] Lead scoring and CRM integration

## References

- LinkedIn Best Practices: https://business.linkedin.com/marketing-solutions/best-practices
- Setup Guide: `../../scripts/LINKEDIN_SETUP.md`
- Auto-Post Script: `../../scripts/linkedin_auto_post.py`
