# Phase 2 Silver Tier - Integration Guide

## Overview

This guide walks you through integrating Silver Tier capabilities into your existing Bronze Tier Digital FTE system.

**Repository**: https://github.com/Aishasiddiqui97/Hackaton-0

---

## Prerequisites

Before starting Silver Tier integration, ensure:

✅ **Bronze Tier is functional**
- Obsidian vault structure exists
- Basic watcher is running
- Agent Skills are defined
- Task workflow works (Inbox → Plans → Done)

✅ **System Requirements**
- Python 3.8+
- Virtual environment activated
- Git installed
- 500MB free disk space

✅ **API Credentials Ready**
- Gmail API credentials (credentials.json)
- LinkedIn account credentials
- WhatsApp Web access
- SMTP server details (for email sending)

---

## Integration Steps

### Step 1: Verify Bronze Tier

```bash
# Check vault structure
ls -la AI_Employee_Vault/
# Should see: Inbox/, Needs_Action/, Plans/, Done/, Skills/

# Check Bronze watcher is working
python AI_Employee_Vault/watcher.py &
# Should start monitoring without errors

# Test basic workflow
echo "Test task" > AI_Employee_Vault/Inbox/test.md
# Should be processed by reasoning engine
```

### Step 2: Install Additional Dependencies

```bash
# Activate virtual environment
cd AI_Employee_Vault
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install Silver Tier dependencies
pip install watchdog>=4.0.0
pip install google-auth>=2.27.0
pip install google-auth-oauthlib>=1.2.0
pip install google-api-python-client>=2.116.0
pip install requests>=2.32.5
pip install beautifulsoup4>=4.12.0
pip install selenium>=4.0.0
pip install webdriver-manager>=4.0.0
pip install python-dotenv>=1.0.0

# Verify installation
pip list | grep -E "watchdog|google-auth|requests|selenium"
```

### Step 3: Configure API Credentials

#### Gmail API Setup

```bash
# 1. Get credentials.json from Google Cloud Console
# 2. Place in project root
cp /path/to/credentials.json .

# 3. First-time authentication
python scripts/gmail_watcher.py
# Browser will open for OAuth consent
# Grant permissions
# token.json will be created automatically
```

#### LinkedIn Setup

```bash
# Add to .env file
cat >> .env << 'EOF'
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_secure_password
EOF
```

#### SMTP Setup (for email sending)

```bash
# Add to .env file
cat >> .env << 'EOF'
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
EOF
```

### Step 4: Test Individual Watchers

#### Test Gmail Watcher

```bash
# Run Gmail watcher
python scripts/gmail_watcher.py

# Check logs
tail -f logs/gmail_actions.log

# Verify: Send yourself a test email
# Should appear in AI_Employee_Vault/Inbox/
```

#### Test LinkedIn Watcher

```bash
# Run LinkedIn watcher
python scripts/linkedin_watcher.py

# Check logs
tail -f logs/linkedin_actions.log

# Verify: Check for LinkedIn notifications
# Should create files in Inbox if notifications exist
```

#### Test WhatsApp Watcher

```bash
# Run WhatsApp watcher (requires QR scan)
python scripts/whatsapp_watcher.py

# Scan QR code with phone
# Check logs
tail -f logs/whatsapp_actions.log
```

### Step 5: Test Reasoning Engine

```bash
# Create a test task
cat > AI_Employee_Vault/Inbox/test_reasoning.md << 'EOF'
# Test Task

Goal: Send email to client@example.com with proposal
Context: Client requested proposal yesterday
Priority: High
EOF

# Run reasoning engine
python AI_Employee_Vault/reasoning_engine.py

# Check output
ls -la AI_Employee_Vault/Needs_Action/
# Should see a Plan.md file with Risk: Medium
```

### Step 6: Test Approval Workflow

```bash
# Find the generated plan
PLAN_FILE=$(ls -t AI_Employee_Vault/Needs_Action/*Plan*.md | head -1)

# Review the plan
cat "$PLAN_FILE"

# Approve the plan
sed -i 's/Approval Status: Pending/Approval Status: Approved/' "$PLAN_FILE"

# Verify approval detected
tail -f logs/silver.log
# Should see approval processing
```

### Step 7: Configure MCP Servers

#### Create Claude Desktop Config

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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
    }
  }
}
```

**Note**: Update paths to match your installation directory.

#### Test MCP Servers

```bash
# Restart Claude Desktop to load MCP config

# In Claude Desktop, test each server:
# "List files in my vault Inbox"
# "Check my unread Gmail"
# "Read my LinkedIn notifications"
```

### Step 8: Start All Watchers

#### Option A: Use Batch Script (Windows)

```bash
# Already created: start_all_watchers.bat
start_all_watchers.bat
```

#### Option B: Manual Start (All Platforms)

```bash
# Terminal 1: Vault Watcher (Bronze)
python AI_Employee_Vault/watcher.py

# Terminal 2: Gmail Watcher
python scripts/gmail_watcher.py

# Terminal 3: LinkedIn Watcher
python scripts/linkedin_watcher.py

# Terminal 4: WhatsApp Watcher
python scripts/whatsapp_watcher.py

# Terminal 5: Scheduler Loop (Silver)
python phase_2_silver/scripts/scheduler_loop.py
```

### Step 9: Configure Automated Startup

#### Windows Task Scheduler

```bash
# Follow guide in SCHEDULER_SETUP.md
# Or run the verification script:
verify_silver_tier.bat
```

#### Linux/Mac Cron

```bash
# Edit crontab
crontab -e

# Add startup job
@reboot cd /path/to/Hackaton-0 && ./start_all_watchers.sh

# Create start script
cat > start_all_watchers.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source AI_Employee_Vault/venv/bin/activate

python AI_Employee_Vault/watcher.py &
python scripts/gmail_watcher.py &
python scripts/linkedin_watcher.py &
python scripts/whatsapp_watcher.py &
python phase_2_silver/scripts/scheduler_loop.py &
EOF

chmod +x start_all_watchers.sh
```

### Step 10: Verify Full Integration

```bash
# Run integration test
python phase_2_silver/scripts/integration_test.py

# Check all components
./verify_silver_tier.bat  # Windows
# or
./verify_silver_tier.sh   # Linux/Mac

# Expected output:
# ✓ Bronze Tier: Operational
# ✓ Vault Structure: Valid
# ✓ Gmail Watcher: Running
# ✓ LinkedIn Watcher: Running
# ✓ WhatsApp Watcher: Running
# ✓ Reasoning Engine: Functional
# ✓ Approval Workflow: Working
# ✓ MCP Servers: Configured
# ✓ Scheduler: Running
# ✓ Silver Tier: 100% Complete
```

---

## Verification Checklist

### Bronze Tier (Foundation)

- [ ] Vault structure exists and is accessible
- [ ] Bronze watcher monitors Inbox
- [ ] Task files are processed
- [ ] Plans are generated
- [ ] Tasks move to Done when completed

### Silver Tier (Extensions)

#### Watchers
- [ ] Gmail watcher detects new emails
- [ ] LinkedIn watcher detects notifications
- [ ] WhatsApp watcher detects messages
- [ ] GitHub watcher detects repo events (if configured)

#### Reasoning & Approval
- [ ] Reasoning engine generates structured plans
- [ ] Risk assessment works correctly
- [ ] Low-risk plans auto-execute
- [ ] Medium/High-risk plans route to Needs_Action
- [ ] Approval status changes are detected
- [ ] Approved plans execute via MCP

#### MCP Integration
- [ ] Claude Desktop recognizes all MCP servers
- [ ] Vault operations work from Claude
- [ ] Email operations work (with approval)
- [ ] LinkedIn operations work (with approval)
- [ ] All MCP calls are logged

#### Automation
- [ ] All watchers start automatically (if configured)
- [ ] Scheduler loop runs continuously
- [ ] System recovers from errors
- [ ] Logs are being written

---

## Troubleshooting

### Common Issues

#### Watchers Not Starting

**Symptom**: Watcher scripts exit immediately

**Solutions**:
```bash
# Check Python path
which python
python --version  # Should be 3.8+

# Check virtual environment
source AI_Employee_Vault/venv/bin/activate

# Check dependencies
pip list | grep watchdog

# Check logs for errors
tail -50 logs/*.log
```

#### API Authentication Failures

**Symptom**: "Authentication failed" errors

**Solutions**:
```bash
# Gmail: Delete token and re-authenticate
rm token.json
python scripts/gmail_watcher.py

# LinkedIn: Check credentials in .env
cat .env | grep LINKEDIN

# SMTP: Verify app password (not regular password)
```

#### Plans Not Generating

**Symptom**: Tasks in Inbox but no plans created

**Solutions**:
```bash
# Check reasoning engine is running
ps aux | grep reasoning_engine

# Check Inbox permissions
ls -la AI_Employee_Vault/Inbox/

# Manually trigger reasoning engine
python AI_Employee_Vault/reasoning_engine.py

# Check logs
tail -50 logs/silver.log
```

#### Approvals Not Processing

**Symptom**: Approved plans not executing

**Solutions**:
```bash
# Verify exact approval text
grep -i "approval status" AI_Employee_Vault/Needs_Action/*.md

# Should be exactly: "Approval Status: Approved"
# Not: "approved", "APPROVED", "Status: Approved"

# Check approval manager logs
tail -50 logs/approvals.log
```

#### MCP Servers Not Responding

**Symptom**: Claude Desktop can't find MCP servers

**Solutions**:
```bash
# Verify config file location
# Windows: %APPDATA%\Claude\claude_desktop_config.json
# Mac: ~/Library/Application Support/Claude/claude_desktop_config.json

# Check paths are absolute (not relative)
cat claude_desktop_config.json

# Restart Claude Desktop completely
# (Quit and reopen, not just close window)

# Test server independently
python mcp_servers/vault_watcher_server.py --test
```

---

## Performance Optimization

### Reduce Polling Frequency

If system is slow or using too many resources:

```python
# Edit watcher scripts
GMAIL_CHECK_INTERVAL = 120  # Increase from 60 to 120 seconds
LINKEDIN_CHECK_INTERVAL = 180  # Increase from 120 to 180 seconds
WHATSAPP_CHECK_INTERVAL = 120  # Increase from 90 to 120 seconds
```

### Disable Unused Watchers

```bash
# Only run watchers you need
# Comment out unused watchers in start_all_watchers.bat
```

### Optimize Logging

```bash
# Reduce log verbosity
# Edit logging configuration in each script
logging.basicConfig(level=logging.WARNING)  # Instead of INFO
```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check system health
./health_check.sh

# Review pending approvals
ls -la AI_Employee_Vault/Needs_Action/

# Check error logs
grep ERROR logs/*.log
```

### Weekly Maintenance

```bash
# Archive old completed tasks
find AI_Employee_Vault/Done/ -name "*.md" -mtime +30 -exec mv {} AI_Employee_Vault/Archive/ \;

# Rotate logs
find logs/ -name "*.log" -size +10M -exec gzip {} \;

# Update dependencies
pip list --outdated
```

### Monthly Review

```bash
# Analyze performance metrics
python phase_2_silver/scripts/analyze_metrics.py

# Review and optimize risk assessment rules
# Review approval patterns
# Update documentation as needed
```

---

## Next Steps

Once Silver Tier is fully operational:

1. **Monitor Performance**: Track metrics for 1-2 weeks
2. **Optimize Workflows**: Adjust based on usage patterns
3. **Train Users**: Document common tasks and workflows
4. **Plan Gold Tier**: Advanced multi-agent coordination
5. **Contribute**: Share improvements with community

---

## Support & Resources

- **Documentation**: `phase_2_silver/README.md`
- **Architecture**: `phase_2_silver/docs/silver_architecture.md`
- **Repository**: https://github.com/Aishasiddiqui97/Hackaton-0
- **Issues**: https://github.com/Aishasiddiqui97/Hackaton-0/issues

---

## Success Criteria

Silver Tier is successfully integrated when:

✅ All watchers run continuously without errors
✅ Tasks are automatically detected and processed
✅ Plans are generated with accurate risk assessment
✅ Approval workflow functions correctly
✅ MCP servers respond to Claude Desktop
✅ System recovers gracefully from errors
✅ All operations are logged for audit
✅ Automated startup works reliably

**Congratulations! You've completed Silver Tier integration! 🎉**
