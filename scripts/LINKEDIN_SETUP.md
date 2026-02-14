# LinkedIn Watcher Setup Guide

## Overview
LinkedIn Watcher monitors your Gmail for LinkedIn notification emails and automatically creates tasks for business relationship management and lead generation.

---

## How It Works

**Email-Based Monitoring:**
- Monitors Gmail for emails from `linkedin.com`
- Parses notification types (connections, messages, profile views, etc.)
- Creates tasks with business context
- Shows desktop notifications
- Triggers AI processing

**No LinkedIn Login Required:**
- Uses existing Gmail authentication
- No need for LinkedIn API access
- No browser automation needed
- Lightweight and reliable

---

## Monitored LinkedIn Events

### 1. Connection Requests 🤝
- New connection invitations
- Creates task with profile review checklist
- Business opportunity assessment

### 2. Messages 💬
- New LinkedIn messages
- Message preview included
- CRM integration suggestions

### 3. Profile Views 👁️
- Who viewed your profile
- Potential lead identification
- Outreach opportunities

### 4. Job Alerts 💼
- Job opportunities
- Career development tracking

### 5. Post Engagement 👍
- Likes, comments, shares on your posts
- Engagement tracking
- Relationship building

### 6. Invitations 📨
- Event invitations
- Group invitations
- Networking opportunities

---

## Setup Instructions

### Prerequisites

✅ Gmail Watcher already configured
✅ Gmail API credentials (credentials.json)
✅ Token.json with Gmail access

**No additional setup needed!** LinkedIn Watcher uses the same Gmail authentication.

---

## Running LinkedIn Watcher

### Start the Watcher

```bash
python scripts/linkedin_watcher.py
```

### Expected Output

```
[2026-02-13 00:40:00] LINKEDIN WATCHER STARTED
[2026-02-13 00:40:00] Gmail API authenticated successfully
[2026-02-13 00:40:00] Loaded 0 previously processed LinkedIn event IDs
[2026-02-13 00:40:01] Found 3 unread LinkedIn notification(s)
[2026-02-13 00:40:01] LINKEDIN_EVENT - CONNECTION - John Doe wants to connect
[2026-02-13 00:40:01] TASK_CREATED - LinkedIn_Connection_20260213_004001.md
[2026-02-13 00:40:01] NOTIFICATION_SHOWN - New Connection Request: John Doe
```

---

## Task Creation

### Connection Request Task Example

```markdown
# 🔔 New Connection Request: John Doe

## Event Details
- **Platform:** LinkedIn
- **Event Type:** Connection
- **Date:** 2026-02-13
- **Message ID:** abc123

## Details
John Doe wants to connect with you on LinkedIn

## Action Items
- [ ] Review their profile
- [ ] Accept or decline connection
- [ ] Send a personalized message if accepting

## Business Context
- **Lead Generation:** Assess if this is a potential business opportunity
- **Relationship Management:** Consider adding to CRM
- **Follow-up:** Set reminder for follow-up if needed
```

---

## Configuration

### Check Interval

Default: 60 seconds (checks every minute)

To change, edit `linkedin_watcher.py`:
```python
CHECK_INTERVAL = 60  # seconds
```

### Notification Settings

Notifications are enabled by default for all LinkedIn events.

---

## Running Multiple Watchers Together

You can run all three watchers simultaneously:

**Terminal 1: Gmail Watcher**
```bash
python scripts/gmail_watcher.py
```

**Terminal 2: GitHub Watcher**
```bash
python scripts/github_watcher.py
```

**Terminal 3: LinkedIn Watcher**
```bash
python scripts/linkedin_watcher.py
```

All three will:
- Monitor their respective platforms
- Create tasks in `AI_Employee_Vault/Needs_Action/`
- Show desktop notifications
- Trigger AI processing
- Log to `logs/actions.log`

---

## Logs

### Main Log
```
logs/actions.log
```

Contains all LinkedIn Watcher activity:
```
[2026-02-13 00:40:00] LINKEDIN WATCHER STARTED
[2026-02-13 00:40:01] LINKEDIN_EVENT - CONNECTION - John Doe
[2026-02-13 00:40:01] TASK_CREATED - LinkedIn_Connection_20260213_004001.md
[2026-02-13 00:40:01] NOTIFICATION_SHOWN - New Connection Request
[2026-02-13 00:40:02] PROCESSOR_SUCCESS - LinkedIn_Connection_20260213_004001.md
```

### Processed Events
```
logs/processed_linkedin_events.txt
```

Tracks processed LinkedIn email IDs to prevent duplicates.

---

## Business Use Cases

### Lead Generation
- Monitor connection requests from potential clients
- Track profile views from target industries
- Identify engagement opportunities

### Relationship Management
- Never miss a LinkedIn message
- Track all interactions automatically
- Build CRM from LinkedIn activity

### Networking
- Stay on top of event invitations
- Monitor post engagement
- Build professional relationships

### Job Opportunities
- Track job alerts automatically
- Never miss relevant opportunities
- Career development tracking

---

## Troubleshooting

### No LinkedIn Notifications Detected

**Possible causes:**
1. No unread LinkedIn emails in Gmail
2. LinkedIn emails in spam/promotions folder
3. All events already processed

**Solution:**
- Check Gmail for unread LinkedIn emails
- Move LinkedIn emails to Primary inbox
- Clear `logs/processed_linkedin_events.txt` to reprocess

### Notifications Not Showing

**Solution:**
- Check Windows notification settings
- Ensure notifications are enabled for PowerShell
- Test with Gmail/GitHub watcher first

### Authentication Failed

**Solution:**
- LinkedIn Watcher uses same Gmail authentication as Gmail Watcher
- If Gmail Watcher works, LinkedIn Watcher will work
- Delete `token.json` and re-authenticate if needed

---

## Integration with Other Watchers

### Complete Digital FTE System

**Gmail Watcher:** General email monitoring
**GitHub Watcher:** Code repository monitoring
**LinkedIn Watcher:** Business relationship monitoring

All three work together to create a complete automated business monitoring system.

---

## Event Type Detection

LinkedIn Watcher intelligently parses email subjects to detect event types:

| Email Subject Pattern | Event Type | Icon |
|----------------------|------------|------|
| "wants to connect" | Connection Request | 🤝 |
| "sent you a message" | Message | 💬 |
| "viewed your profile" | Profile View | 👁️ |
| "job alert" | Job Alert | 💼 |
| "liked your post" | Post Engagement | 👍 |
| "invited you" | Invitation | 📨 |

---

## Best Practices

1. **Check LinkedIn regularly** - Watcher creates tasks, but you should review LinkedIn directly
2. **Respond promptly** - Use tasks as reminders for timely responses
3. **Update CRM** - Add valuable connections to your CRM system
4. **Track opportunities** - Use tasks to track business opportunities
5. **Engage authentically** - Don't automate responses, use AI for insights only

---

## Security & Privacy

- **No LinkedIn login required** - Uses Gmail only
- **Read-only access** - Cannot send LinkedIn messages
- **Local processing** - All data stays on your machine
- **No data sharing** - LinkedIn data not sent to external services

---

## Stopping the Watcher

**Keyboard Interrupt:**
```
Ctrl + C
```

**Kill Process:**
```bash
tasklist | findstr python
taskkill /F /PID <process_id>
```

---

## Support

If you encounter issues:
1. Check `logs/actions.log` for errors
2. Verify Gmail authentication works
3. Test with Gmail Watcher first
4. Ensure LinkedIn emails are in Gmail inbox
