# 🥇 Gold Tier Quick Start Guide

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Claude Desktop installed
- [ ] Odoo Community Edition installed (optional but recommended)
- [ ] Facebook Business Page (for Facebook/Instagram)
- [ ] Twitter Developer Account (for Twitter/X)
- [ ] All API credentials ready

---

## Step 1: Install Dependencies

```bash
cd "E:\Python.py\Hackaton 0"
cd AI_Employee_Vault
python -m venv venv
venv\Scripts\activate
pip install -r ../requirements.txt
```

---

## Step 2: Configure Environment Variables

1. Copy the template:
```bash
copy .env.template .env
```

2. Edit `.env` and fill in your credentials:
   - Odoo: URL, database, username, password
   - Facebook: Access token, Page ID
   - Instagram: Access token, Account ID
   - Twitter: Bearer token, API keys, Access tokens

---

## Step 3: Set Up Odoo (Optional)

### Install Odoo Community Edition:

**Option A: Docker (Recommended)**
```bash
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:15
docker run -p 8069:8069 --name odoo --link db:db -t odoo
```

**Option B: Native Installation**
1. Download from https://www.odoo.com/page/download
2. Install and run
3. Create database named "odoo"
4. Install Accounting module

### Configure Odoo:
1. Access http://localhost:8069
2. Create database: `odoo`
3. Install "Accounting" module
4. Create test customer and products
5. Note admin password for `.env`

---

## Step 4: Configure Social Media APIs

### Facebook & Instagram:

1. Go to https://developers.facebook.com
2. Create App → Business Type
3. Add "Facebook Login" and "Instagram Basic Display"
4. Get Page Access Token:
   - Graph API Explorer
   - Select your Page
   - Generate token with permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `instagram_basic`
     - `instagram_content_publish`
5. Get Page ID and Instagram Account ID
6. Add to `.env`

### Twitter (X):

1. Apply for Developer Account: https://developer.twitter.com
2. Create Project and App
3. Enable OAuth 1.0a
4. Generate API Keys and Access Tokens
5. Request Elevated Access (for posting)
6. Add all credentials to `.env`

---

## Step 5: Configure Claude Desktop MCP Servers

Edit Claude Desktop config:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add all 9 MCP servers:

```json
{
  "mcpServers": {
    "vault-watcher": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\vault_watcher_server.py"]
    },
    "gmail-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\gmail_server.py"]
    },
    "email-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\email_server.py"]
    },
    "linkedin-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\linkedin_server.py"]
    },
    "whatsapp-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\whatsapp_server.py"]
    },
    "odoo-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\odoo_server.py"]
    },
    "facebook-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\facebook_server.py"]
    },
    "instagram-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\instagram_server.py"]
    },
    "twitter-server": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\twitter_server.py"]
    }
  }
}
```

Restart Claude Desktop.

---

## Step 6: Validate Installation

Run the validation script:

```bash
python scripts\validate_gold_tier.py
```

Expected output:
```
✅ Passed: 10
❌ Failed: 0
🎉 All tests passed! Gold Tier is ready.
```

---

## Step 7: Start the System

### Option A: Automated Start
```bash
start_gold_tier.bat
```

### Option B: Manual Start
```bash
# Terminal 1: Vault Watcher
python AI_Employee_Vault\watcher.py

# Terminal 2: Gmail Watcher
python AI_Employee_Vault\scripts\gmail_watcher.py

# Terminal 3: LinkedIn Watcher
python scripts\linkedin_watcher.py

# Terminal 4: WhatsApp Watcher
python scripts\whatsapp_watcher.py
```

---

## Step 8: Generate First CEO Briefing

```bash
python scripts\ceo_briefing_generator.py
```

Check output in: `AI_Employee_Vault\CEO_Briefings\`

---

## Step 9: Schedule Weekly CEO Briefing

### Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "CEO Weekly Briefing"
4. Trigger: Weekly, Monday, 8:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `scripts\ceo_briefing_generator.py`
   - Start in: `E:\Python.py\Hackaton 0`
6. Finish

---

## Step 10: Test Each Component

### Test Odoo:
```bash
python -c "from mcp_servers.odoo_server import OdooMCPServer; s = OdooMCPServer(); print('Odoo:', s.ensure_authenticated())"
```

### Test Facebook:
Create test file: `AI_Employee_Vault\Inbox\test_facebook.md`
```markdown
# Facebook Post Test

Post to Facebook: "Testing Gold Tier integration! 🚀"

Risk Level: Medium
```

### Test Instagram:
Create test file: `AI_Employee_Vault\Inbox\test_instagram.md`
```markdown
# Instagram Post Test

Post to Instagram:
Image: https://picsum.photos/1080/1080
Caption: "Beautiful automation! #goldtier #ai"

Risk Level: Medium
```

### Test Twitter:
Create test file: `AI_Employee_Vault\Inbox\test_twitter.md`
```markdown
# Twitter Post Test

Tweet: "Just completed Gold Tier implementation! 🥇 #automation #ai"

Risk Level: Medium
```

---

## Monitoring & Logs

Check logs in real-time:

```bash
# All logs
tail -f logs\*.log

# Specific component
tail -f logs\odoo_actions.log
tail -f logs\facebook_actions.log
tail -f logs\instagram_actions.log
tail -f logs\twitter_actions.log
tail -f logs\ceo_briefing.log
```

---

## Troubleshooting

### Odoo Connection Failed
- Verify Odoo is running: http://localhost:8069
- Check credentials in `.env`
- Ensure Accounting module installed

### Facebook/Instagram API Errors
- Verify token hasn't expired
- Check permissions in Facebook Developer Console
- Ensure Page/Account IDs are correct

### Twitter API Errors
- Verify Elevated Access granted
- Check all 5 credentials in `.env`
- Ensure OAuth 1.0a enabled

### CEO Briefing Empty
- Run validation script first
- Check individual MCP server logs
- Verify all credentials configured

---

## Success Indicators

You'll know Gold Tier is working when:

✅ All 4 watchers running without errors
✅ All 9 MCP servers connected in Claude Desktop
✅ Test posts appear on social media
✅ Odoo invoices created successfully
✅ CEO Briefing generates with real data
✅ All logs show successful operations
✅ Approval workflow functioning

---

## Next Steps

1. **Customize Content:** Update Skills for your business
2. **Optimize Posting:** Adjust schedules based on analytics
3. **Monitor Performance:** Review CEO Briefings weekly
4. **Scale Operations:** Add more platforms as needed
5. **Refine Automation:** Improve based on insights

---

## Support

- **Documentation:** See `GOLD_TIER_DOCUMENTATION.md`
- **Issues:** Check logs in `logs/` directory
- **Validation:** Run `python scripts\validate_gold_tier.py`

---

**Congratulations! Your Gold Tier Digital FTE is operational! 🎉**
