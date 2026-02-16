# Phase 2: Silver Tier Architecture

## Overview

This phase extends the Bronze Tier foundation with advanced automation capabilities while maintaining clean separation of concerns.

**Repository**: https://github.com/Aishasiddiqui97/Hackaton-0

---

## Phase Separation Philosophy

### Bronze Tier (Foundation)
- Core Obsidian vault structure
- Basic file system monitoring
- Manual task processing
- Simple Agent Skills framework

### Silver Tier (This Phase)
- Multi-channel watchers (Gmail, LinkedIn, WhatsApp, GitHub)
- Automated plan generation with reasoning engine
- Risk-based human approval workflow
- MCP server integration for external actions
- Continuous scheduler loop

**Key Principle**: Silver extends Bronze without modifying it. All Bronze functionality remains intact and operational.

---

## Architecture

```
phase_2_silver/
├── skills/                    # Agent Skills (AI-driven capabilities)
│   ├── gmail-watcher/        # Email monitoring skill
│   ├── linkedin-watcher/     # LinkedIn notification skill
│   ├── whatsapp-watcher/     # WhatsApp monitoring skill
│   ├── plan-generator/       # Automated Plan.md creation
│   ├── approval-manager/     # Human-in-the-loop workflow
│   └── mcp-orchestrator/     # MCP server coordination
│
├── mcp_servers/              # Model Context Protocol servers
│   ├── email-server/         # Email sending capability
│   ├── linkedin-server/      # LinkedIn posting capability
│   ├── gmail-server/         # Gmail API integration
│   ├── whatsapp-server/      # WhatsApp integration
│   └── vault-watcher/        # Vault monitoring server
│
├── scripts/                  # Automation scripts
│   └── scheduler_loop.py     # Continuous reasoning loop
│
└── docs/                     # Documentation
    └── silver_architecture.md
```

---

## How Silver Extends Bronze

### Reused Components
1. **Logging System**: All Silver actions log to Bronze's `logs/` directory
2. **Inbox System**: Silver watchers write to `AI_Employee_Vault/Inbox/`
3. **Vault Structure**: Uses existing `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`
4. **Agent Skills**: Extends Bronze's Task_Reader, Task_Processor, Task_Closer

### New Capabilities
1. **Multi-Channel Monitoring**: Watches Gmail, LinkedIn, WhatsApp, GitHub
2. **Reasoning Engine**: Automatically generates structured Plan.md files
3. **Risk Detection**: Classifies tasks as Low/Medium/High risk
4. **Approval Workflow**: Routes risky tasks to `/Needs_Action` for human review
5. **MCP Integration**: Executes approved actions via MCP servers
6. **Scheduler Loop**: Continuous autonomous operation

---

## Plan.md Structure (Silver Enhancement)

All Silver-generated plans follow this structure:

```markdown
# Plan: [Task Title]

**Goal**: [What needs to be accomplished]

**Context**: [Background information and reasoning]

**Steps**:
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]

**Risk Level**: [Low | Medium | High]

**Approval Required**: [Yes | No]

**Approval Status**: [Pending | Approved | Rejected]

**Status**: [Planning | In Progress | Completed | Failed]
```

---

## Human Approval Flow

### Risk-Based Routing

**Low Risk** → Auto-execute
- Reading files
- Generating reports
- Moving files within vault

**Medium/High Risk** → Requires approval
- Sending emails
- Posting to social media
- Modifying external systems
- Financial transactions

### Approval Process

1. **Detection**: Reasoning engine identifies risk level
2. **Routing**: Plan.md moved to `AI_Employee_Vault/Needs_Action/`
3. **Notification**: User notified via system log
4. **Review**: Human reviews plan and updates `Approval Status: Approved`
5. **Execution**: MCP server executes approved action
6. **Completion**: Task moved to `/Done`

---

## Running Silver Tier

### Prerequisites

1. Bronze Tier must be functional
2. Python 3.8+ with virtual environment
3. API credentials configured (.env file)
4. Task Scheduler configured (Windows) or cron (Linux)

### Installation

```bash
# Activate Bronze virtual environment
cd AI_Employee_Vault
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install Silver dependencies (if any new ones)
pip install -r requirements.txt
```

### Start All Watchers

**Windows**:
```bash
start_all_watchers.bat
```

**Manual Start**:
```bash
# Terminal 1: Core vault watcher
python AI_Employee_Vault/watcher.py

# Terminal 2: Gmail watcher
python phase_2_silver/skills/gmail-watcher/gmail_watcher.py

# Terminal 3: LinkedIn watcher
python phase_2_silver/skills/linkedin-watcher/linkedin_watcher.py

# Terminal 4: WhatsApp watcher
python phase_2_silver/skills/whatsapp-watcher/whatsapp_watcher.py
```

### Continuous Scheduler Loop

```bash
python phase_2_silver/scripts/scheduler_loop.py
```

This runs a continuous loop that:
1. Monitors all input channels
2. Detects new tasks
3. Generates plans
4. Executes approved steps
5. Re-evaluates and continues

---

## Logging

All Silver actions log to:

- `logs/actions.log` - General action log
- `logs/silver.log` - Silver-specific events
- `logs/gmail_actions.log` - Gmail operations
- `logs/linkedin_actions.log` - LinkedIn operations

**Log Format**:
```
[YYYY-MM-DD HH:MM:SS] [PHASE] ACTION - Status
```

Example:
```
[2026-02-16 10:30:45] [SILVER] GMAIL_WATCHER - New email detected: "Project Update"
[2026-02-16 10:30:46] [SILVER] PLAN_GENERATOR - Created Plan: 20260216-103046-Plan.md
[2026-02-16 10:30:47] [SILVER] APPROVAL_MANAGER - Routed to Needs_Action (Risk: Medium)
```

---

## Integration with Claude Desktop

Silver Tier MCP servers can be configured in Claude Desktop's config:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "vault-watcher": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\phase_2_silver\\mcp_servers\\vault-watcher\\server.py"]
    },
    "gmail": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\phase_2_silver\\mcp_servers\\gmail-server\\server.py"]
    },
    "linkedin": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\phase_2_silver\\mcp_servers\\linkedin-server\\server.py"]
    }
  }
}
```

---

## Testing Silver Tier

### 1. Test Watcher Detection

Drop a test file in Inbox:
```bash
echo "Test task for Silver Tier" > AI_Employee_Vault/Inbox/test_silver.md
```

### 2. Test Plan Generation

Check that `reasoning_engine.py` creates a Plan.md in `/Plans` or `/Needs_Action`

### 3. Test Approval Flow

Create a high-risk task and verify it routes to `/Needs_Action`:
```markdown
# High Risk Task

Goal: Send email to all clients
Context: Marketing campaign
Risk Level: High
```

### 4. Test MCP Integration

Approve a plan and verify the MCP server executes the action.

---

## Troubleshooting

### Watchers Not Starting
- Check virtual environment is activated
- Verify API credentials in `.env`
- Check logs for error messages

### Plans Not Generating
- Ensure `reasoning_engine.py` is running
- Check `AI_Employee_Vault/Inbox/` has new files
- Verify file permissions

### Approval Not Working
- Confirm plan has `Approval Status: Approved` (exact text)
- Check plan is in `/Needs_Action` folder
- Verify MCP server is running

### MCP Servers Not Responding
- Restart Claude Desktop
- Check MCP server logs
- Verify config paths are absolute

---

## Next Steps: Gold Tier

Silver Tier prepares the foundation for Gold Tier, which adds:
- Advanced multi-agent coordination
- Proactive task generation
- Learning from past executions
- Complex workflow orchestration
- Full autonomous operation

---

## Contributing

See main repository: https://github.com/Aishasiddiqui97/Hackaton-0

## License

Same as parent project.
