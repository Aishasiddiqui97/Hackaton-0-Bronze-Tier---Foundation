# Digital FTE - Silver Tier foundation

Welcome to the **Digital FTE Silver Tier foundation** repository. This project is a fully operational autonomous assistant system designed to monitor multiple communication channels (Senses), process information (Reasoning), and execute actions via MCP servers (Acting).

## 🚀 Overview

The Digital FTE (Full-Time Equivalent) implements a robust "Sense-Reason-Act" loop. It scans your Inbox for new signals, uses a specialized reasoning engine to determine risk and plan actions, and executes those actions through standardized Model Context Protocol (MCP) servers.

### Key Integration Features:
- **Multi-Channel Monitoring**: Automated watchers for Gmail, LinkedIn, and WhatsApp.
- **Autonomous Reasoning**: An engine that clearing the `Inbox` using the "Ralph Wiggum" loop.
- **Safety Gating**: Automated risk detection for Medium and High risk tasks, requiring human-in-the-loop approval.
- **Standardized MCP Servers**: Five dedicated servers for Vault, Gmail, LinkedIn, WhatsApp, and Email actions.
- **Unified Logging**: Standardized, timestamped, and separated logs for full traceability.

---

## 📂 Project Structure

```text
├── AI_Employee_Vault/       # The core "Brain" and data storage
│   ├── Inbox/               # Incoming signals/tasks
│   ├── Plans/               # Generated execution plans
│   ├── Needs_Action/        # Tasks awaiting human approval
│   ├── Done/                # Completed tasks
│   ├── scripts/             # Core logic scripts (Gmail, Engine, etc.)
│   └── watcher.py           # Main vault monitor
├── mcp_servers/             # MCP Servers for Claude/Assistant integration
│   ├── gmail_server.py      # Gmail search & stats
│   ├── linkedin_server.py   # LinkedIn posting
│   ├── whatsapp_server.py   # WhatsApp messaging
│   ├── email_server.py      # Secure email sending
│   └── vault_watcher_server.py # System controls
├── scripts/                 # Channel-specific watchers (LinkedIn, WhatsApp)
├── logs/                    # Standardized log files
└── README.md                # You are here!
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10+
- [Git](https://git-scm.com/)
- [Claude Desktop](https://claude.ai/download) (for MCP integration)

### 2. Install Dependencies
```bash
pip install google-auth google-auth-oauthlib google-api-python-client watchdog plyer
```

### 3. Configuration
- **Gmail/LinkedIn**: Place your `credentials.json` in the root (for Gmail API).
- **GitHub**: Configure your repo in `AI_Employee_Vault/scripts/github_config.json`.
- **Secrets**: Ensure no secrets are tracked by Git (check `.gitignore`).

---

## 🏃 Running the System

### Step 1: Start the Vault Watcher (Main Engine)
This script monitors the file system and triggers the reasoning engine.
```bash
python AI_Employee_Vault/watcher.py
```

### Step 2: Start the Sensors (Watchers)
Run these in separate terminal windows to monitor your channels:
```bash
# Gmail
python AI_Employee_Vault/scripts/gmail_watcher.py

# LinkedIn
python scripts/linkedin_watcher.py

# WhatsApp
python scripts/whatsapp_watcher.py
```

### Step 3: MCP Servers
Enable the servers in your Claude Desktop configuration or run them manually:
```bash
python mcp_servers/vault_watcher_server.py
# (And others in the mcp_servers/ folder)
```

---

## 🛡️ Safety & Risk Gating

The system automatically detects risk levels:
- **Low Risk**: Information gathering, internal logging. Executes automatically.
- **Medium/High Risk**: Email sending, public posts, messaging. Moves to `AI_Employee_Vault/Needs_Action/` and requires you to change the status to `Approved` in the `.md` file.

---

## 📊 Logging
Logs are separated for easy debugging:
- `logs/gmail_actions.log`
- `logs/linkedin_actions.log`
- `logs/whatsapp_actions.log`
- `logs/actions.log` (Vault & System)

---

Developed with ❤️ as part of the **Hackathon 0 Silver Tier Foundation**.
