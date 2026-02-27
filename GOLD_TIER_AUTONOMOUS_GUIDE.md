# 🏆 Gold Tier Autonomous Social Media Agent

## Ralph Wiggum Loop Pattern - Always-On Operation

Your autonomous AI agent that manages social media and WhatsApp 24/7 without asking "What should I do next?"

## 📁 Folder Structure (Auto-Created)

```
00_Inbox/
├── Social_Media/          # Incoming social media tasks
├── WhatsApp/             # WhatsApp messages to process
└── Urgent_WhatsApp.md    # Urgent messages flagged for you

01_Drafts/
└── Auto_Generated/       # AI-generated drafts

02_Pending_Approvals/
├── Social_Posts/         # Posts waiting for your approval
└── Email_Drafts/         # Email drafts for approval

03_Posted/
└── History/              # Posted content archive
```

## 🚀 How to Start

### Quick Start
```powershell
.\start_autonomous_agent.bat
```

### Manual Start
```powershell
python autonomous_social_agent.py
```

## 🤖 What the Agent Does Automatically

### 1. Social Media Post Generation (Every 6 Hours)
- **Platforms**: LinkedIn, Twitter, Facebook, Instagram
- **Source**: Company_Handbook.md for context
- **Output**: Platform-specific posts in `02_Pending_Approvals/Social_Posts/`
- **Tone**: Professional yet engaging
- **Hashtags**: Platform-appropriate (3-5 for LinkedIn/FB, 15+ for Instagram)
- **CTA**: Always included for sales generation

### 2. WhatsApp Auto-Reply
**Routine Queries** (Auto-replied):
- Greetings (Hello, Hi, Hey)
- General info requests
- Basic pricing inquiries

**Urgent Queries** (Flagged for you):
- Contains: "Urgent", "Price Quote", "Meeting", "ASAP", "Emergency"
- Action: Moved to `00_Inbox/Urgent_WhatsApp.md`
- Notification: Logged for your attention

### 3. Auto-Posting Workflow
1. Agent generates post → Saves to `02_Pending_Approvals/Social_Posts/`
2. You review and approve → Move to `03_Posted/History/`
3. Agent detects move → Auto-posts via API
4. Agent marks as posted → Renames with `POSTED_` prefix

### 4. Error Handling
- API errors logged to `00_Inbox/Error_Log.md`
- Agent continues to next platform
- No interruption to autonomous operation

## 📋 Platform-Specific Configurations

### LinkedIn
- **Tone**: Professional and thought-leadership
- **Hashtags**: 3-5
- **Max Length**: 3000 characters
- **CTA**: "Connect with us to learn more"

### Twitter
- **Tone**: Concise and engaging
- **Hashtags**: 2-3
- **Max Length**: 280 characters
- **CTA**: "Follow for more insights"

### Facebook
- **Tone**: Friendly and conversational
- **Hashtags**: 4-5
- **Max Length**: 5000 characters
- **CTA**: "Like and share if you agree"

### Instagram
- **Tone**: Visual and inspiring
- **Hashtags**: 15-20
- **Max Length**: 2200 characters
- **CTA**: "Double tap if you love this"

## 🔄 The Ralph Wiggum Loop

```
┌─────────────────────────────────────────┐
│  1. Scan 00_Inbox folders               │
│     ↓                                   │
│  2. Reason about tasks                  │
│     ↓                                   │
│  3. Execute (Generate/Reply/Post)       │
│     ↓                                   │
│  4. Verify output                       │
│     ↓                                   │
│  5. Log action                          │
│     ↓                                   │
│  6. Wait 30 minutes                     │
│     ↓                                   │
│  7. Repeat (Never stops)                │
└─────────────────────────────────────────┘
```

## 🎯 Human-in-the-Loop (HITL)

### When Agent Needs Your Approval
- All social media posts (in `02_Pending_Approvals/Social_Posts/`)
- Sensitive financial transactions
- Final content before posting

### When Agent Acts Autonomously
- WhatsApp routine replies
- Content generation
- Auto-posting approved content
- Error logging and recovery

## 📊 Content Generation Topics

Agent rotates through these topics:
1. Innovation in business
2. Customer success stories
3. Industry insights
4. Team achievements
5. Product updates
6. Thought leadership

## 🔐 Safety Features

### No Direct Posting Without Approval
- All posts go to `02_Pending_Approvals/` first
- You must move to `03_Posted/` to trigger posting
- Two-step verification process

### Urgent Message Detection
- Keywords: "Urgent", "Price Quote", "Meeting", "ASAP", "Emergency"
- Automatically flagged and moved to urgent folder
- No auto-reply for sensitive queries

### Error Recovery
- Errors logged to `Error_Log.md`
- Agent continues operation
- No system crash or halt

## 📈 Monitoring the Agent

### Check Status
```powershell
# View logs
type logs\autonomous_agent.log

# Check last posts
type logs\last_social_posts.json

# View pending approvals
dir 02_Pending_Approvals\Social_Posts

# Check posted history
dir 03_Posted\History
```

### Agent Activity Indicators
- ✅ Post generated
- 📤 Auto-posted
- 🚨 Urgent message flagged
- ❌ Error logged
- 🔄 Iteration complete

## 🛠️ Customization

### Change Post Interval
Edit `autonomous_social_agent.py`:
```python
POST_INTERVAL_HOURS = 6  # Change to your preference
```

### Add More Platforms
Add to `PLATFORMS` list:
```python
PLATFORMS = ['LinkedIn', 'Twitter', 'Facebook', 'Instagram', 'TikTok']
```

### Modify Content Topics
Edit `topics` list in `generate_social_post()` method

### Adjust Loop Frequency
Change sleep time in `ralph_wiggum_loop()`:
```python
time.sleep(1800)  # 1800 = 30 minutes
```

## 🎓 Workflow Examples

### Example 1: Social Media Post
```
1. Agent generates LinkedIn post at 9 AM
2. Saves to: 02_Pending_Approvals/Social_Posts/LinkedIn_Post_20260225_090000.md
3. You review and approve
4. You move to: 03_Posted/History/LinkedIn_Post_20260225_090000.md
5. Agent detects move (next iteration)
6. Agent posts via API
7. Agent renames: POSTED_LinkedIn_Post_20260225_090000.md
8. Logged in: logs/autonomous_agent.log
```

### Example 2: WhatsApp Auto-Reply
```
1. Message arrives: "Hello, I need information about your services"
2. Saved to: 00_Inbox/WhatsApp/message_001.md
3. Agent detects (next iteration)
4. Agent identifies: Routine query
5. Agent generates reply: "We'd be happy to share more information..."
6. Saves: 00_Inbox/WhatsApp/message_001_REPLIED.md
7. Original deleted
8. Logged in: logs/autonomous_agent.log
```

### Example 3: Urgent WhatsApp
```
1. Message arrives: "URGENT: Need price quote for meeting tomorrow"
2. Saved to: 00_Inbox/WhatsApp/urgent_message.md
3. Agent detects (next iteration)
4. Agent identifies: Contains "URGENT" and "price quote"
5. Agent moves to: 00_Inbox/Urgent_WhatsApp_urgent_message.md
6. Agent logs: "🚨 URGENT WhatsApp message"
7. You get notified
8. You handle manually
```

## 🚦 Starting and Stopping

### Start Agent
```powershell
.\start_autonomous_agent.bat
```

### Stop Agent
Press `Ctrl+C` in the terminal

### Run as Background Service (Advanced)
```powershell
# Using Windows Task Scheduler
# Or use the service scripts from your existing setup
```

## 📚 Integration with Existing System

### Works With
- ✅ Your existing MCP servers
- ✅ Company_Handbook.md for context
- ✅ Existing folder structure
- ✅ Your approval workflow

### Complements
- ✅ Gmail watcher
- ✅ LinkedIn watcher
- ✅ GitHub watcher
- ✅ Task processor
- ✅ Odoo integration

## ✅ Success Checklist

- [ ] Folders created automatically
- [ ] Agent started: `.\start_autonomous_agent.bat`
- [ ] First posts generated in `02_Pending_Approvals/Social_Posts/`
- [ ] WhatsApp messages being processed
- [ ] Logs updating in `logs/autonomous_agent.log`
- [ ] Approved posts auto-posting
- [ ] Urgent messages flagged correctly

## 🎉 You're All Set!

Your Gold Tier Autonomous Agent is now running 24/7:
- ✅ Generating social media posts every 6 hours
- ✅ Auto-replying to routine WhatsApp queries
- ✅ Flagging urgent messages for your attention
- ✅ Auto-posting approved content
- ✅ Logging all actions
- ✅ Never asking "What should I do next?"

**The Ralph Wiggum Loop is active!** 🤖

---

**Questions?** Check logs: `logs/autonomous_agent.log`

**Need help?** Review error log: `00_Inbox/Error_Log.md`

**Ready to scale?** Add more platforms and customize topics!
