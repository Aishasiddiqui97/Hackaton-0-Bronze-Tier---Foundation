# 🏆 Gold Tier Autonomous System - Complete Guide

## Full Automation - Ralph Wiggum Loop Mode

### What You Get
- ✅ **Auto-posting**: LinkedIn, Twitter, Facebook, Instagram
- ✅ **Auto-generation**: New posts every 12 hours
- ✅ **Odoo Integration**: Dashboard updates Monday 8 AM
- ✅ **System Monitoring**: Live status tracking
- ✅ **Error Handling**: Automatic recovery
- ✅ **Never Stops**: Ralph Wiggum Loop (autonomous)

## 🚀 Quick Start (3 Commands)

### 1. Create Hello World Test Posts
```powershell
python test_hello_world.py
```

### 2. Start Gold Tier System
```powershell
.\start_gold_tier_system.bat
```

### 3. Check System Status
```powershell
type System_Live_Status.md
```

## 📊 System Features

### Automatic Post Generation
- **Frequency**: Every 12 hours
- **Platforms**: LinkedIn, Twitter, Facebook, Instagram
- **Source**: Company_Handbook.md
- **Output**: 02_Pending_Approvals/Social_Posts/

### Automatic Posting
- **Check Interval**: Every 15 minutes
- **Process**: Detects approved posts → Auto-posts → Renames with POSTED_
- **Platforms**: All configured platforms

### Odoo Integration
- **Schedule**: Monday 8 AM
- **Action**: Fetch accounting summary
- **Output**: Updates Dashboard.md

### System Monitoring
- **File**: System_Live_Status.md
- **Updates**: Every iteration
- **Shows**: Platform status, metrics, next actions

## 🎯 Folder Structure

```
00_Inbox/
├── Urgent_WhatsApp/          # Urgent messages
└── ALERTS.md                 # System alerts

01_Drafts/
└── Auto_Generated/           # Auto-generated drafts

02_Pending_Approvals/
├── Social_Posts/             # Posts awaiting approval
└── Email_Drafts/             # Email drafts

03_Posted/
└── History/                  # Posted content
    ├── POSTED_*.md          # Successfully posted
    └── *.md                 # Pending posting

System_Live_Status.md         # Live system status
System_Errors.md              # Error log
```

## 🔄 The Ralph Wiggum Loop

```
┌─────────────────────────────────────────┐
│  Every 15 minutes:                      │
│                                         │
│  1. Update System_Live_Status.md        │
│  2. Check if 12 hours passed            │
│     → Generate new posts                │
│  3. Scan 03_Posted/History/             │
│     → Auto-post approved content        │
│  4. Check if Monday 8 AM                │
│     → Update Odoo dashboard             │
│  5. Log all actions                     │
│  6. Repeat forever                      │
└─────────────────────────────────────────┘
```

## 📋 Platform Status

### LinkedIn
- **Method**: Playwright (browser automation)
- **Status**: ✅ Working
- **Credentials**: Email/Password in .env

### Twitter/X
- **Method**: OAuth 1.0a (Tweepy)
- **Status**: ⚠️ Requires valid API keys
- **Credentials**: API keys in .env

### Facebook
- **Method**: Graph API
- **Status**: ⚠️ Requires valid access token
- **Credentials**: Access token in .env

### Instagram
- **Method**: Graph API
- **Status**: ⚠️ Requires image + valid token
- **Credentials**: Access token in .env

### Odoo
- **Method**: JSON-RPC
- **Status**: ✅ Working (if Odoo running)
- **Credentials**: URL/DB/User/Pass in .env

## 🎓 Usage Examples

### Start System
```powershell
.\start_gold_tier_system.bat
```

### Check Status
```powershell
type System_Live_Status.md
```

### View Errors
```powershell
type System_Errors.md
```

### View Alerts
```powershell
type 00_Inbox\ALERTS.md
```

### Manual Post Generation
```powershell
.\generate_all_posts.bat
```

### Check Post Status
```powershell
.\check_post_status.bat
```

## ⚙️ Configuration

### Post Generation Interval
Edit `gold_tier_autonomous.py`:
```python
self.post_generation_interval = 43200  # 12 hours (in seconds)
```

### Check Interval
```python
self.check_interval = 900  # 15 minutes (in seconds)
```

### Odoo Dashboard Schedule
```python
if now.weekday() != 0 or now.hour != 8:  # Monday at 8 AM
```

## 🔐 Required Credentials (.env)

```env
# LinkedIn
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password

# Twitter (Optional)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret

# Facebook (Optional)
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id

# Instagram (Optional)
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_account_id

# Odoo (Optional)
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

## 📈 Monitoring

### System Status
```powershell
type System_Live_Status.md
```

Shows:
- Platform connectivity
- Last check time
- Next post generation
- Active processes

### Error Log
```powershell
type System_Errors.md
```

Shows:
- Failed posts
- API errors
- System issues

### Alerts
```powershell
type 00_Inbox\ALERTS.md
```

Shows:
- Critical failures
- Manual intervention needed

## 🎯 Workflow

### Automatic (No Action Needed)
1. System generates posts every 12 hours
2. Posts saved to 02_Pending_Approvals/Social_Posts/
3. You review and move to 03_Posted/History/
4. System auto-posts every 15 minutes
5. Files renamed with POSTED_ prefix

### Manual Approval
```powershell
# Review posts
dir 02_Pending_Approvals\Social_Posts

# Approve by moving
move "02_Pending_Approvals\Social_Posts\*.md" "03_Posted\History\"

# System will auto-post in next iteration (max 15 min)
```

## 🐛 Troubleshooting

### System Not Posting
1. Check System_Live_Status.md
2. Verify platform status (✅ or ❌)
3. Check System_Errors.md for errors
4. Verify credentials in .env

### Posts Not Generating
1. Check last_post_generation time
2. Wait for 12-hour interval
3. Or manually run: `.\generate_all_posts.bat`

### Odoo Not Updating
1. Verify Odoo is running: http://localhost:8069
2. Check credentials in .env
3. Wait for Monday 8 AM
4. Or manually test: `python odoo_test_api.py`

## ✅ Success Checklist

- [ ] All folders created
- [ ] .env file configured
- [ ] Hello World posts created
- [ ] Gold Tier System started
- [ ] System_Live_Status.md updating
- [ ] LinkedIn auto-posting working
- [ ] Posts generating every 12 hours
- [ ] Error logging functional

## 🎉 You're All Set!

Your Gold Tier Autonomous System is now:
- ✅ Running 24/7
- ✅ Auto-generating posts every 12 hours
- ✅ Auto-posting to all platforms
- ✅ Monitoring system health
- ✅ Logging errors and alerts
- ✅ Never asking "What should I do next?"

## 🚀 Start Now

```powershell
# 1. Test connectivity
python test_hello_world.py

# 2. Start system
.\start_gold_tier_system.bat

# 3. Monitor status
type System_Live_Status.md
```

---

**The Ralph Wiggum Loop is now active! 🏆**
