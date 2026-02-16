# Silver Tier Architecture Documentation

## System Design Philosophy

Silver Tier implements a **multi-agent autonomous system** that extends Bronze's manual workflow with intelligent automation while preserving human oversight for critical decisions.

---

## Core Components

### 1. Watcher Skills (Input Layer)

**Purpose**: Monitor external channels and convert events into actionable tasks

#### Gmail Watcher
- **Location**: `phase_2_silver/skills/gmail-watcher/`
- **Function**: Monitors Gmail inbox via Google API
- **Output**: Creates task files in `AI_Employee_Vault/Inbox/`
- **Trigger**: Polls every 60 seconds
- **Risk**: Low (read-only operation)

#### LinkedIn Watcher
- **Location**: `phase_2_silver/skills/linkedin-watcher/`
- **Function**: Monitors LinkedIn notifications and messages
- **Output**: Creates notification files in Inbox
- **Trigger**: Polls every 120 seconds
- **Risk**: Low (read-only operation)

#### WhatsApp Watcher
- **Location**: `phase_2_silver/skills/whatsapp-watcher/`
- **Function**: Monitors WhatsApp messages (via web interface)
- **Output**: Creates message files in Inbox
- **Trigger**: Polls every 90 seconds
- **Risk**: Low (read-only operation)

#### GitHub Watcher
- **Location**: Integrated with existing `scripts/`
- **Function**: Monitors repository events (pushes, PRs, issues)
- **Output**: Creates event files in Inbox
- **Trigger**: Webhook or polling
- **Risk**: Low (read-only operation)

---

### 2. Reasoning Engine (Processing Layer)

**Purpose**: Analyze tasks, generate execution plans, assess risk

#### Plan Generator Skill
- **Location**: `phase_2_silver/skills/plan-generator/`
- **Function**: Converts raw tasks into structured Plan.md files
- **Input**: Files from `AI_Employee_Vault/Inbox/`
- **Output**: Plan.md files in `/Plans` or `/Needs_Action`
- **Logic**:
  1. Read task file
  2. Analyze intent and requirements
  3. Break down into actionable steps
  4. Assess risk level (Low/Medium/High)
  5. Determine if approval needed
  6. Generate structured plan
  7. Route to appropriate folder

#### Risk Assessment Algorithm

```python
def assess_risk(task_content):
    high_risk_keywords = [
        'send email', 'post', 'publish', 'delete', 'payment',
        'transfer', 'purchase', 'deploy', 'production'
    ]

    medium_risk_keywords = [
        'modify', 'update', 'change', 'create', 'add',
        'remove', 'edit', 'configure'
    ]

    content_lower = task_content.lower()

    if any(keyword in content_lower for keyword in high_risk_keywords):
        return "High"
    elif any(keyword in content_lower for keyword in medium_risk_keywords):
        return "Medium"
    else:
        return "Low"
```

---

### 3. Approval Manager (Control Layer)

**Purpose**: Implement human-in-the-loop for risky operations

#### Approval Manager Skill
- **Location**: `phase_2_silver/skills/approval-manager/`
- **Function**: Manages approval workflow for Medium/High risk tasks
- **Process**:
  1. Monitor `/Needs_Action` folder
  2. Detect when `Approval Status: Approved` is added
  3. Validate approval format
  4. Move approved plan to execution queue
  5. Log approval event

#### Approval States

| State | Description | Next Action |
|-------|-------------|-------------|
| Pending | Awaiting human review | Wait |
| Approved | Human approved execution | Execute via MCP |
| Rejected | Human rejected task | Move to Done with rejection note |
| Expired | No response after 24h | Move to Done with timeout note |

---

### 4. MCP Orchestrator (Execution Layer)

**Purpose**: Coordinate MCP server calls for approved actions

#### MCP Orchestrator Skill
- **Location**: `phase_2_silver/skills/mcp-orchestrator/`
- **Function**: Routes approved plans to appropriate MCP servers
- **Logic**:
  1. Read approved plan
  2. Identify required action (email, post, etc.)
  3. Select appropriate MCP server
  4. Format request payload
  5. Call MCP server
  6. Handle response
  7. Update plan status
  8. Move to Done

#### MCP Server Mapping

```python
ACTION_TO_SERVER = {
    'send_email': 'email-server',
    'post_linkedin': 'linkedin-server',
    'read_gmail': 'gmail-server',
    'send_whatsapp': 'whatsapp-server',
    'monitor_vault': 'vault-watcher'
}
```

---

## Data Flow

```
External Event (Email/LinkedIn/WhatsApp/GitHub)
    ↓
Watcher Skill detects event
    ↓
Creates task file in /Inbox
    ↓
Vault Watcher (Bronze) detects new file
    ↓
Reasoning Engine analyzes task
    ↓
Plan Generator creates Plan.md
    ↓
Risk Assessment
    ↓
    ├─→ Low Risk → /Plans → Auto-execute
    └─→ Medium/High Risk → /Needs_Action → Wait for approval
                                ↓
                        Human reviews and approves
                                ↓
                        Approval Manager detects approval
                                ↓
                        MCP Orchestrator executes action
                                ↓
                        Task moved to /Done
```

---

## Logging Architecture

### Log Files

| File | Purpose | Format |
|------|---------|--------|
| `logs/actions.log` | All system actions | `[timestamp] [PHASE] ACTION - details` |
| `logs/silver.log` | Silver-specific events | `[timestamp] [SILVER] component - event` |
| `logs/gmail_actions.log` | Gmail operations | `[timestamp] [GMAIL] action - result` |
| `logs/linkedin_actions.log` | LinkedIn operations | `[timestamp] [LINKEDIN] action - result` |
| `logs/whatsapp_actions.log` | WhatsApp operations | `[timestamp] [WHATSAPP] action - result` |

### Log Levels

- **INFO**: Normal operations (task detected, plan created)
- **WARNING**: Unusual but handled (duplicate task, missing field)
- **ERROR**: Failures requiring attention (API error, file not found)
- **CRITICAL**: System failures (watcher crash, MCP server down)

---

## State Management

### Task States

1. **Detected**: Watcher found new event
2. **Ingested**: Task file created in Inbox
3. **Analyzed**: Reasoning engine processed task
4. **Planned**: Plan.md generated
5. **Pending Approval**: Waiting in Needs_Action
6. **Approved**: Human approved execution
7. **Executing**: MCP server processing
8. **Completed**: Moved to Done
9. **Failed**: Error occurred, logged

### State Persistence

- Task state tracked via file location and Plan.md status field
- No database required (filesystem is the database)
- Atomic operations via file moves
- Idempotent processing (can safely retry)

---

## Error Handling

### Retry Logic

```python
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds

def execute_with_retry(action, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            return action()
        except Exception as e:
            if attempt < max_retries - 1:
                log_warning(f"Attempt {attempt+1} failed: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_error(f"All retries failed: {e}")
                raise
```

### Failure Recovery

- Failed tasks logged with full error details
- Plans marked with `Status: Failed` and error message
- Human can review and manually retry or reject
- System continues processing other tasks

---

## Performance Considerations

### Polling Intervals

- Gmail: 60s (API quota: 250 quota units/user/second)
- LinkedIn: 120s (rate limit: ~100 requests/hour)
- WhatsApp: 90s (web scraping, be gentle)
- Vault: 5s (local filesystem, fast)

### Resource Usage

- Each watcher: ~50MB RAM
- Reasoning engine: ~100MB RAM
- Total system: ~300MB RAM
- CPU: Minimal (mostly I/O bound)

### Scalability

- Current design: Single machine, ~100 tasks/day
- Bottleneck: Human approval for Medium/High risk
- Future: Multi-agent coordination for parallel processing

---

## Security Model

### Credential Management

- All API keys in `.env` file (gitignored)
- OAuth tokens in `token.json` (gitignored)
- No credentials in code or logs
- Credentials loaded at runtime only

### Risk Mitigation

- Human approval required for external actions
- Read-only operations auto-approved
- Write operations require explicit approval
- All actions logged for audit trail

### Data Privacy

- Email content stored locally only
- No data sent to external services except approved actions
- Sensitive data redacted in logs
- User controls all data retention

---

## Integration Points

### Bronze Tier Integration

- **Reuses**: Vault structure, logging, Agent Skills framework
- **Extends**: Adds automated plan generation, approval workflow
- **Preserves**: All Bronze functionality remains unchanged

### Claude Desktop Integration

- MCP servers expose capabilities to Claude Desktop
- Claude can read vault, generate plans, execute approved actions
- Bidirectional: Watchers feed Claude, Claude executes via MCP

### Future Gold Tier

- Silver provides foundation for multi-agent coordination
- Approval workflow enables autonomous learning
- Logging enables performance analysis and optimization

---

## Monitoring & Observability

### Health Checks

```bash
# Check if all watchers are running
ps aux | grep watcher

# Check recent log activity
tail -f logs/silver.log

# Check pending approvals
ls -la AI_Employee_Vault/Needs_Action/

# Check completed tasks today
find AI_Employee_Vault/Done/ -name "*.md" -mtime -1
```

### Metrics to Track

- Tasks processed per day
- Average time from detection to completion
- Approval rate (approved vs rejected)
- Error rate by component
- API quota usage

---

## Maintenance

### Daily
- Review `/Needs_Action` for pending approvals
- Check logs for errors
- Verify watchers are running

### Weekly
- Archive old tasks from `/Done`
- Review and optimize polling intervals
- Update API credentials if needed

### Monthly
- Analyze performance metrics
- Optimize risk assessment rules
- Update documentation

---

## Troubleshooting Guide

### Watcher Not Detecting Events

1. Check API credentials are valid
2. Verify network connectivity
3. Check API quota not exceeded
4. Review watcher logs for errors

### Plans Not Being Generated

1. Verify reasoning_engine.py is running
2. Check Inbox has new files
3. Review reasoning engine logs
4. Verify file permissions

### Approvals Not Processing

1. Check exact text: `Approval Status: Approved`
2. Verify plan is in `/Needs_Action`
3. Check approval_manager is running
4. Review approval logs

### MCP Server Errors

1. Restart Claude Desktop
2. Verify MCP config paths
3. Check MCP server logs
4. Test server independently

---

## References

- Bronze Tier: `AI_Employee_Vault/README.md`
- MCP Protocol: https://modelcontextprotocol.io
- Repository: https://github.com/Aishasiddiqui97/Hackaton-0
