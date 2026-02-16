# Silver Tier Quick Reference

Quick reference guide for common operations and commands in the Digital FTE Silver Tier system.

---

## 🚀 Starting the System

### Windows (Automated)
```bash
start_all_watchers.bat
```

### Manual Start (All Platforms)
```bash
# Terminal 1: Core vault watcher
python AI_Employee_Vault/watcher.py

# Terminal 2: Gmail watcher
python scripts/gmail_watcher.py

# Terminal 3: LinkedIn watcher
python scripts/linkedin_watcher.py

# Terminal 4: WhatsApp watcher
python scripts/whatsapp_watcher.py

# Terminal 5: Scheduler loop
python phase_2_silver/scripts/scheduler_loop.py
```

---

## 📋 Common Tasks

### Check System Status
```bash
# Check running watchers
ps aux | grep watcher

# Check recent logs
tail -20 logs/silver.log

# Check pending approvals
ls -la AI_Employee_Vault/Needs_Action/

# Check completed tasks today
find AI_Employee_Vault/Done/ -name "*.md" -mtime -1
```

### Approve a Plan
```bash
# 1. Find the plan
ls -la AI_Employee_Vault/Needs_Action/

# 2. Edit the plan
nano AI_Employee_Vault/Needs_Action/PLAN_FILE.md

# 3. Change this line:
# FROM: Approval Status: Pending
# TO:   Approval Status: Approved

# 4. Save and exit (Ctrl+X, Y, Enter)
```

### Create a Manual Task
```bash
# Create task file
cat > AI_Employee_Vault/Inbox/my_task.md << 'EOF'
# My Task

Goal: [What you want to accomplish]
Context: [Background information]
Priority: [High/Medium/Low]

## Details
[Task details here]
EOF
```

### Check Logs
```bash
# All logs
tail -f logs/*.log

# Specific component
tail -f logs/gmail_actions.log
tail -f logs/linkedin_actions.log
tail -f logs/whatsapp_actions.log
tail -f logs/silver.log

# Search for errors
grep ERROR logs/*.log

# Search for approvals
grep APPROVED logs/approvals.log
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Gmail
GMAIL_CHECK_INTERVAL=60

# LinkedIn
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_CHECK_INTERVAL=120

# WhatsApp
WHATSAPP_CHECK_INTERVAL=90

# SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
```

### Claude Desktop MCP Config
**Location**: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

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

---

## 🛡️ Risk Levels

### Low Risk (Auto-approved)
- Reading files
- Generating reports
- Internal operations
- Logging

### Medium Risk (Requires approval)
- Sending emails to known contacts
- Posting to social media
- Modifying configuration
- API calls

### High Risk (Requires explicit approval)
- Financial transactions
- Sending emails to new contacts
- Deleting data
- Production deployments

---

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Inbox/          # New tasks arrive here
├── Plans/          # Low-risk plans (auto-execute)
├── Needs_Action/   # Medium/High-risk plans (need approval)
└── Done/           # Completed tasks
```

---

## 🔍 Troubleshooting

### Watcher Not Starting
```bash
# Check Python version
python --version  # Should be 3.8+

# Activate virtual environment
cd AI_Employee_Vault
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Check dependencies
pip list | grep watchdog
```

### Authentication Failed
```bash
# Gmail: Delete token and re-auth
rm token.json
python scripts/gmail_watcher.py

# LinkedIn: Check .env
cat .env | grep LINKEDIN
```

### Plans Not Generating
```bash
# Check reasoning engine
ps aux | grep reasoning_engine

# Manually trigger
python AI_Employee_Vault/reasoning_engine.py

# Check logs
tail -50 logs/silver.log
```

### Approvals Not Processing
```bash
# Verify exact text (case-sensitive!)
grep "Approval Status" AI_Employee_Vault/Needs_Action/*.md

# Must be exactly: "Approval Status: Approved"
# NOT: "approved", "APPROVED", "Status: Approved"
```

---

## 📊 Monitoring Commands

### System Health
```bash
# Check all watchers running
ps aux | grep -E "watcher|scheduler"

# Check disk space
df -h

# Check memory usage
free -h  # Linux
```

### Performance Metrics
```bash
# Tasks processed today
find AI_Employee_Vault/Done/ -name "*.md" -mtime -1 | wc -l

# Pending approvals
ls AI_Employee_Vault/Needs_Action/*.md 2>/dev/null | wc -l

# Error count today
grep ERROR logs/*.log | grep "$(date +%Y-%m-%d)" | wc -l
```

### Log Analysis
```bash
# Most common errors
grep ERROR logs/*.log | cut -d'-' -f4- | sort | uniq -c | sort -rn | head -10

# Approval rate
TOTAL=$(grep "APPROVAL_MANAGER" logs/approvals.log | wc -l)
APPROVED=$(grep "APPROVED" logs/approvals.log | wc -l)
echo "Approval rate: $((APPROVED * 100 / TOTAL))%"

# Tasks by source
grep "Source:" AI_Employee_Vault/Done/*.md | cut -d':' -f3 | sort | uniq -c
```

---

## 🔄 Maintenance

### Daily
```bash
# Check pending approvals
ls -la AI_Employee_Vault/Needs_Action/

# Review error logs
grep ERROR logs/*.log | tail -20

# Verify watchers running
ps aux | grep watcher
```

### Weekly
```bash
# Archive old tasks (30+ days)
find AI_Employee_Vault/Done/ -name "*.md" -mtime +30 -exec mv {} AI_Employee_Vault/Archive/ \;

# Rotate large logs (>10MB)
find logs/ -name "*.log" -size +10M -exec gzip {} \;

# Check disk space
du -sh AI_Employee_Vault/
```

### Monthly
```bash
# Update dependencies
pip list --outdated

# Review performance metrics
python phase_2_silver/scripts/analyze_metrics.py

# Backup vault
tar -czf vault_backup_$(date +%Y%m%d).tar.gz AI_Employee_Vault/
```

---

## 🎯 Common Workflows

### Email Response Workflow
```
1. Gmail Watcher detects email
2. Creates task in Inbox
3. Reasoning Engine generates plan
4. Plan routed to Needs_Action (Risk: Medium)
5. Human reviews and approves
6. Email Server sends response
7. Task moved to Done
```

### LinkedIn Post Workflow
```
1. Create post draft in Needs_Action
2. Add "Approval Status: Approved"
3. LinkedIn Auto-Post publishes
4. Post URL logged
5. Task moved to Done
```

### Manual Task Workflow
```
1. Create task file in Inbox
2. Reasoning Engine generates plan
3. If low risk: Auto-execute
4. If medium/high risk: Route to Needs_Action
5. Human approves (if needed)
6. MCP Orchestrator executes
7. Task moved to Done
```

---

## 🔑 Keyboard Shortcuts (Claude Desktop)

```
Ctrl+K          Open command palette
Ctrl+Shift+P    MCP server commands
Ctrl+L          Clear conversation
Ctrl+N          New conversation
```

---

## 📞 Quick Help

### Documentation
- Main: `README.md`
- Silver: `phase_2_silver/README.md`
- Integration: `phase_2_silver/docs/INTEGRATION_GUIDE.md`
- Architecture: `phase_2_silver/docs/silver_architecture.md`

### Skills
- Gmail: `phase_2_silver/skills/gmail-watcher/README.md`
- LinkedIn: `phase_2_silver/skills/linkedin-watcher/README.md`
- WhatsApp: `phase_2_silver/skills/whatsapp-watcher/README.md`
- Plan Generator: `phase_2_silver/skills/plan-generator/README.md`
- Approval Manager: `phase_2_silver/skills/approval-manager/README.md`
- MCP Orchestrator: `phase_2_silver/skills/mcp-orchestrator/README.md`

### MCP Servers
- Email: `phase_2_silver/mcp_servers/email-server/README.md`
- LinkedIn: `phase_2_silver/mcp_servers/linkedin-server/README.md`
- Gmail: `phase_2_silver/mcp_servers/gmail-server/README.md`
- WhatsApp: `phase_2_silver/mcp_servers/whatsapp-server/README.md`
- Vault: `phase_2_silver/mcp_servers/vault-watcher/README.md`

### Support
- Repository: https://github.com/Aishasiddiqui97/Hackaton-0
- Issues: https://github.com/Aishasiddiqui97/Hackaton-0/issues

---

## 💡 Pro Tips

1. **Use exact approval text**: `Approval Status: Approved` (case-sensitive)
2. **Check logs first**: Most issues show up in logs
3. **Start small**: Test with low-risk tasks first
4. **Monitor regularly**: Check Needs_Action folder daily
5. **Keep credentials safe**: Never commit .env or token files
6. **Backup regularly**: Archive vault monthly
7. **Update dependencies**: Check for updates weekly
8. **Read documentation**: Each component has detailed docs
9. **Test in isolation**: Test each watcher independently first
10. **Use Claude Desktop**: MCP integration makes everything easier

---

**Quick Reference Version**: 1.0
**Last Updated**: 2026-02-16
**Status**: Silver Tier Complete ✅
