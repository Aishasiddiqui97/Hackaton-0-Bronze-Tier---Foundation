# Digital FTE - Tiered Autonomous Assistant System

Welcome to the **Digital FTE (Full-Time Equivalent)** repository - a fully operational autonomous assistant system with tiered capabilities from foundation to advanced automation.

**Repository**: https://github.com/Aishasiddiqui97/Hackaton-0

---

## 🎯 Project Overview

The Digital FTE implements a robust "Sense-Reason-Act" loop across multiple tiers of sophistication. It monitors communication channels (Senses), processes information with risk assessment (Reasoning), and executes actions through standardized MCP servers (Acting).

### Tiered Architecture

This project is organized into achievement tiers, allowing you to build progressively more sophisticated capabilities:

#### 🥉 Bronze Tier: Foundation (✅ Complete)
- Obsidian vault with structured folders
- Basic file system monitoring
- Manual task processing
- Agent Skills framework
- Simple logging

#### 🥈 Silver Tier: Functional Assistant (✅ Complete)
- Multi-channel watchers (Gmail, LinkedIn, WhatsApp, GitHub)
- Automated plan generation with reasoning engine
- Risk-based human approval workflow
- 5 MCP servers for external actions
- Continuous scheduler loop
- Automated startup via Task Scheduler

#### 🥇 Gold Tier: Advanced Automation (🚧 Future)
- Multi-agent coordination
- Proactive task generation
- Learning from past executions
- Complex workflow orchestration
- Full autonomous operation

---

## 📂 Project Structure

```text
Hackaton-0/
│
├── phase_2_silver/              # Silver Tier organized components
│   ├── README.md                # Silver Tier documentation
│   ├── skills/                  # Agent Skills (AI capabilities)
│   │   ├── gmail-watcher/       # Email monitoring skill
│   │   ├── linkedin-watcher/    # LinkedIn monitoring skill
│   │   ├── whatsapp-watcher/    # WhatsApp monitoring skill
│   │   ├── plan-generator/      # Automated planning skill
│   │   ├── approval-manager/    # Human-in-the-loop workflow
│   │   └── mcp-orchestrator/    # MCP server coordination
│   │
│   ├── mcp_servers/             # MCP Server documentation
│   │   ├── email-server/        # Email sending capability
│   │   ├── linkedin-server/     # LinkedIn posting capability
│   │   ├── gmail-server/        # Gmail API integration
│   │   ├── whatsapp-server/     # WhatsApp integration
│   │   └── vault-watcher/       # Vault monitoring server
│   │
│   ├── scripts/                 # Automation scripts
│   │   └── scheduler_loop.py    # Continuous reasoning loop
│   │
│   └── docs/                    # Documentation
│       ├── silver_architecture.md
│       └── INTEGRATION_GUIDE.md
│
├── AI_Employee_Vault/           # Core "Brain" and data storage (Bronze)
│   ├── Inbox/                   # Incoming signals/tasks
│   ├── Plans/                   # Generated execution plans
│   ├── Needs_Action/            # Tasks awaiting human approval
│   ├── Done/                    # Completed tasks
│   ├── Skills/                  # Agent skill definitions
│   ├── scripts/                 # Core logic scripts
│   │   └── gmail_watcher.py     # Gmail monitoring
│   ├── watcher.py               # Main vault monitor (Bronze)
│   ├── reasoning_engine.py      # Plan generation engine
│   └── task_processor.py        # Task execution
│
├── mcp_servers/                 # MCP Server implementations
│   ├── gmail_server.py          # Gmail search & stats
│   ├── linkedin_server.py       # LinkedIn posting
│   ├── whatsapp_server.py       # WhatsApp messaging
│   ├── email_server.py          # Secure email sending
│   └── vault_watcher_server.py  # System controls
│
├── scripts/                     # Channel-specific watchers
│   ├── gmail_watcher.py         # Gmail monitoring
│   ├── linkedin_watcher.py      # LinkedIn monitoring
│   ├── linkedin_auto_post.py    # LinkedIn auto-posting
│   ├── whatsapp_watcher.py      # WhatsApp monitoring
│   └── github_watcher.py        # GitHub monitoring
│
├── logs/                        # Standardized log files
│   ├── gmail_actions.log
│   ├── linkedin_actions.log
│   ├── whatsapp_actions.log
│   ├── silver.log
│   └── actions.log
│
├── start_all_watchers.bat       # Windows startup script
├── SCHEDULER_SETUP.md           # Automated startup guide
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- Claude Desktop (for MCP integration)
- API credentials (Gmail, LinkedIn, etc.)

### Installation

```bash
# Clone repository
git clone https://github.com/Aishasiddiqui97/Hackaton-0.git
cd Hackaton-0

# Create virtual environment
cd AI_Employee_Vault
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Gmail API**: Place `credentials.json` in project root
2. **LinkedIn**: Add credentials to `.env` file
3. **SMTP**: Configure email sending in `.env`
4. **WhatsApp**: QR code scan on first run

See `phase_2_silver/docs/INTEGRATION_GUIDE.md` for detailed setup.

### Running the System

#### Option 1: Automated (Windows)
```bash
start_all_watchers.bat
```

#### Option 2: Manual Start
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

## 🔑 Key Features

### Multi-Channel Monitoring (Senses)
- **Gmail**: Monitors inbox for new emails via Google API
- **LinkedIn**: Tracks notifications and messages
- **WhatsApp**: Monitors messages via WhatsApp Web
- **GitHub**: Watches repository events (pushes, PRs, issues)

### Autonomous Reasoning (Brain)
- **Plan Generation**: Automatically creates structured execution plans
- **Risk Assessment**: Classifies tasks as Low/Medium/High risk
- **Approval Routing**: Routes risky tasks to human review
- **Context Analysis**: Understands task intent and requirements

### Action Execution (Acting)
- **MCP Servers**: 5 standardized servers for external actions
- **Email Sending**: SMTP-based email with approval validation
- **LinkedIn Posting**: Automated posting with content approval
- **Vault Operations**: Read/write access to knowledge base

### Safety & Compliance
- **Human-in-the-Loop**: Medium/High risk tasks require approval
- **Audit Trail**: All actions logged with timestamps
- **Credential Security**: API keys in .env (gitignored)
- **Approval Validation**: Strict format checking

---

## 🛡️ Risk-Based Approval Workflow

### Risk Levels

**Low Risk** (Auto-approved)
- Reading files or data
- Generating reports
- Internal operations
- Logging and monitoring

**Medium Risk** (Requires approval)
- Sending emails to known contacts
- Posting to social media
- Modifying configuration
- API calls to external services

**High Risk** (Requires explicit approval)
- Financial transactions
- Sending emails to new contacts
- Deleting data
- Production deployments

### Approval Process

```
Task detected → Plan generated → Risk assessed
    ↓
Low Risk: Auto-execute
    ↓
Medium/High Risk: Move to Needs_Action
    ↓
Human reviews and approves
    ↓
MCP server executes action
    ↓
Task moved to Done
```

To approve a plan:
1. Open plan file in `AI_Employee_Vault/Needs_Action/`
2. Review the plan details
3. Change `Approval Status: Pending` to `Approval Status: Approved`
4. Save the file
5. System automatically executes

---

## 📊 Logging & Monitoring

### Log Files

All operations are logged to separate files for easy debugging:

- `logs/gmail_actions.log` - Gmail operations
- `logs/linkedin_actions.log` - LinkedIn operations
- `logs/whatsapp_actions.log` - WhatsApp operations
- `logs/silver.log` - Silver Tier events
- `logs/approvals.log` - Approval decisions
- `logs/actions.log` - General system actions

### Log Format

```
[YYYY-MM-DD HH:MM:SS] [COMPONENT] LEVEL - Message
```

Example:
```
[2026-02-16 10:30:45] [GMAIL_WATCHER] INFO - New email detected: "Project Update"
[2026-02-16 10:30:46] [PLAN_GENERATOR] INFO - Created Plan: 20260216-103046-Plan.md
[2026-02-16 10:30:47] [APPROVAL_MANAGER] INFO - Routed to Needs_Action (Risk: Medium)
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Gmail API
GMAIL_CHECK_INTERVAL=60

# LinkedIn
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_CHECK_INTERVAL=120

# WhatsApp
WHATSAPP_CHECK_INTERVAL=90

# SMTP (for email sending)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
```

### Claude Desktop MCP Configuration

Add to Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

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

## 📖 Documentation

### Getting Started
- **Bronze Tier**: `AI_Employee_Vault/README.md`
- **Silver Tier**: `phase_2_silver/README.md`
- **Integration Guide**: `phase_2_silver/docs/INTEGRATION_GUIDE.md`
- **Architecture**: `phase_2_silver/docs/silver_architecture.md`

### Skills Documentation
- Gmail Watcher: `phase_2_silver/skills/gmail-watcher/README.md`
- LinkedIn Watcher: `phase_2_silver/skills/linkedin-watcher/README.md`
- WhatsApp Watcher: `phase_2_silver/skills/whatsapp-watcher/README.md`
- Plan Generator: `phase_2_silver/skills/plan-generator/README.md`
- Approval Manager: `phase_2_silver/skills/approval-manager/README.md`
- MCP Orchestrator: `phase_2_silver/skills/mcp-orchestrator/README.md`

### MCP Servers Documentation
- Email Server: `phase_2_silver/mcp_servers/email-server/README.md`
- LinkedIn Server: `phase_2_silver/mcp_servers/linkedin-server/README.md`
- Gmail Server: `phase_2_silver/mcp_servers/gmail-server/README.md`
- WhatsApp Server: `phase_2_silver/mcp_servers/whatsapp-server/README.md`
- Vault Watcher: `phase_2_silver/mcp_servers/vault-watcher/README.md`

---

## 🧪 Testing

### Manual Testing

```bash
# Test individual components
python -m pytest tests/

# Test Gmail watcher
python scripts/gmail_watcher.py --test

# Test reasoning engine
echo "Test task" > AI_Employee_Vault/Inbox/test.md

# Test approval workflow
# (Create plan, approve it, verify execution)
```

### Integration Testing

```bash
# Run full integration test
python phase_2_silver/scripts/integration_test.py

# Verify Silver Tier completion
./verify_silver_tier.bat  # Windows
```

---

## 🔒 Security

### Credential Management
- All API keys stored in `.env` (gitignored)
- OAuth tokens in `token.json` (gitignored)
- No credentials in code or logs
- Session files encrypted

### Approval Requirements
- Human approval for external actions
- Read-only operations auto-approved
- All actions logged for audit
- Approval format strictly validated

### Data Privacy
- All data stored locally
- No cloud sync without explicit approval
- Sensitive data redacted in logs
- User controls all data retention

---

## 🚧 Troubleshooting

### Common Issues

**Watchers not starting**
- Check Python version (3.8+)
- Verify virtual environment is activated
- Check dependencies are installed
- Review logs for errors

**API authentication failures**
- Delete token files and re-authenticate
- Verify credentials in `.env`
- Check API quotas not exceeded

**Plans not generating**
- Ensure reasoning engine is running
- Check Inbox has new files
- Verify file permissions
- Review reasoning engine logs

**Approvals not processing**
- Use exact text: `Approval Status: Approved`
- Check plan is in `/Needs_Action`
- Verify approval manager is running

See `phase_2_silver/docs/INTEGRATION_GUIDE.md` for detailed troubleshooting.

---

## 🎯 Roadmap

### Completed ✅
- Bronze Tier: Foundation
- Silver Tier: Functional Assistant
- Multi-channel monitoring
- Automated plan generation
- Risk-based approval workflow
- MCP server integration
- Automated scheduling

### In Progress 🚧
- Performance optimization
- Enhanced error handling
- Additional MCP servers

### Planned 📋
- Gold Tier: Advanced automation
- Multi-agent coordination
- Machine learning integration
- Advanced analytics dashboard
- Mobile app for approvals

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See issues at: https://github.com/Aishasiddiqui97/Hackaton-0/issues

---

## 📄 License

This project is part of Hackathon 0 and is provided as-is for educational and development purposes.

---

## 🙏 Acknowledgments

- Built with Claude Code and Claude Opus 4.6
- MCP Protocol by Anthropic
- Inspired by the Digital FTE concept
- Community contributions and feedback

---

## 📞 Support

- **Documentation**: See `phase_2_silver/` folder
- **Issues**: https://github.com/Aishasiddiqui97/Hackaton-0/issues
- **Repository**: https://github.com/Aishasiddiqui97/Hackaton-0

---

**Status**: Silver Tier Complete ✅ | Bronze Tier Complete ✅ | Gold Tier Planned 📋

Developed with ❤️ as part of **Hackathon 0 - Digital FTE Silver Tier Foundation**
