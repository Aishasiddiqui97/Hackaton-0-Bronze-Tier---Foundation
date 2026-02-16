# MCP Orchestrator Skill

## Purpose
Coordinates execution of approved plans by routing actions to appropriate MCP (Model Context Protocol) servers, managing the execution lifecycle, and handling responses.

## Type
**Execution Skill** - Action orchestration agent

## Risk Level
**Medium** - Executes external actions, but only after approval

## Implementation
**Location**: Integrated into `../../AI_Employee_Vault/task_processor.py` and MCP server clients

## Functionality

### What It Does
1. Monitors approved plans ready for execution
2. Parses plan steps to identify required actions
3. Maps actions to appropriate MCP servers
4. Formats requests according to MCP protocol
5. Executes actions via MCP server calls
6. Handles responses and errors
7. Updates plan status throughout execution
8. Logs all MCP interactions
9. Moves completed plans to Done folder

### MCP Server Mapping

```python
ACTION_TO_SERVER = {
    # Email operations
    'send_email': 'email-server',
    'read_gmail': 'gmail-server',
    'search_email': 'gmail-server',

    # Social media operations
    'post_linkedin': 'linkedin-server',
    'read_linkedin': 'linkedin-server',

    # Messaging operations
    'send_whatsapp': 'whatsapp-server',
    'read_whatsapp': 'whatsapp-server',

    # Vault operations
    'read_vault': 'vault-watcher',
    'write_vault': 'vault-watcher',
    'monitor_vault': 'vault-watcher',

    # Future servers
    'calendar_event': 'calendar-server',
    'slack_message': 'slack-server',
}
```

## MCP Protocol Integration

### Server Configuration

MCP servers are configured in Claude Desktop config:

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

### Request Format

MCP requests follow standardized format:

```python
mcp_request = {
    "server": "email-server",
    "action": "send_email",
    "parameters": {
        "to": "client@example.com",
        "subject": "Q4 Proposal",
        "body": "Please find attached...",
        "attachments": ["docs/proposal.pdf"]
    },
    "metadata": {
        "plan_id": "20260216-141530-Plan",
        "task_id": "gmail-19b6fdde257c24a2",
        "risk_level": "Medium",
        "approved_by": "user@company.com",
        "timestamp": "2026-02-16T14:20:30Z"
    }
}
```

### Response Handling

```python
mcp_response = {
    "status": "success",  # or "error", "partial"
    "message": "Email sent successfully",
    "data": {
        "message_id": "abc123",
        "sent_at": "2026-02-16T14:20:35Z",
        "recipients": ["client@example.com"]
    },
    "errors": []  # Empty if successful
}
```

## Execution Flow

### Step-by-Step Process

```
Approved plan detected
    ↓
MCP Orchestrator reads plan
    ↓
Parse steps and identify actions
    ↓
For each action:
    ├─→ Identify required MCP server
    ├─→ Validate server is available
    ├─→ Format request payload
    ├─→ Call MCP server
    ├─→ Wait for response
    ├─→ Handle response (success/error)
    ├─→ Update plan status
    └─→ Log interaction
    ↓
All steps completed
    ↓
Update plan: Status = Completed
    ↓
Move plan to Done folder
    ↓
Log completion
```

### Parallel vs Sequential Execution

**Sequential** (default)
- Execute steps one at a time
- Wait for each to complete before next
- Safer, easier to debug
- Used for dependent steps

**Parallel** (optional)
- Execute independent steps simultaneously
- Faster for non-dependent actions
- Requires careful coordination
- Used for bulk operations

```python
def execute_plan(plan, mode='sequential'):
    if mode == 'sequential':
        for step in plan.steps:
            result = execute_step(step)
            if not result.success:
                handle_error(result)
                break
    elif mode == 'parallel':
        results = execute_steps_parallel(plan.steps)
        handle_results(results)
```

## Action Parsing

### Extracting Actions from Plans

```python
def parse_plan_actions(plan_content):
    """
    Extracts actionable steps from plan and maps to MCP servers.
    """
    actions = []

    # Extract steps section
    steps_section = extract_section(plan_content, "Steps")

    for step in steps_section:
        # Identify action type
        action_type = identify_action_type(step)

        # Map to MCP server
        server = ACTION_TO_SERVER.get(action_type)

        if server:
            actions.append({
                'step': step,
                'action_type': action_type,
                'server': server,
                'parameters': extract_parameters(step)
            })

    return actions
```

### Action Type Detection

```python
def identify_action_type(step_text):
    """
    Determines what type of action a step requires.
    """
    step_lower = step_text.lower()

    # Email actions
    if 'send email' in step_lower or 'email to' in step_lower:
        return 'send_email'
    if 'read email' in step_lower or 'check email' in step_lower:
        return 'read_gmail'

    # LinkedIn actions
    if 'post to linkedin' in step_lower or 'publish on linkedin' in step_lower:
        return 'post_linkedin'

    # WhatsApp actions
    if 'send whatsapp' in step_lower or 'message on whatsapp' in step_lower:
        return 'send_whatsapp'

    # Vault actions
    if 'read from vault' in step_lower or 'check vault' in step_lower:
        return 'read_vault'
    if 'write to vault' in step_lower or 'save to vault' in step_lower:
        return 'write_vault'

    # Default: no MCP action needed (internal operation)
    return None
```

## MCP Server Communication

### Server Health Check

```python
def check_server_health(server_name):
    """
    Verifies MCP server is running and responsive.
    """
    try:
        response = mcp_call(server_name, 'health_check', {})
        return response.status == 'healthy'
    except Exception as e:
        log_error(f"Server {server_name} health check failed: {e}")
        return False
```

### Retry Logic

```python
def execute_with_retry(server, action, parameters, max_retries=3):
    """
    Executes MCP action with automatic retry on failure.
    """
    for attempt in range(max_retries):
        try:
            response = mcp_call(server, action, parameters)

            if response.status == 'success':
                return response

            # Retry on transient errors
            if response.status == 'error' and is_transient_error(response):
                log_warning(f"Attempt {attempt+1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue

            # Non-transient error, don't retry
            return response

        except Exception as e:
            if attempt < max_retries - 1:
                log_warning(f"Attempt {attempt+1} exception: {e}, retrying...")
                time.sleep(2 ** attempt)
            else:
                log_error(f"All retries failed: {e}")
                raise

    return create_error_response("Max retries exceeded")
```

### Error Handling

```python
def handle_mcp_error(error_response, plan, step):
    """
    Handles errors from MCP server calls.
    """
    error_type = error_response.get('error_type')

    if error_type == 'authentication':
        # Credential issue
        log_error("Authentication failed - check credentials")
        update_plan_status(plan, "Failed - Authentication Error")
        notify_user("MCP authentication failed")

    elif error_type == 'rate_limit':
        # Rate limiting
        log_warning("Rate limit hit - will retry later")
        schedule_retry(plan, delay=3600)  # Retry in 1 hour

    elif error_type == 'validation':
        # Invalid parameters
        log_error(f"Invalid parameters: {error_response.message}")
        update_plan_status(plan, "Failed - Invalid Parameters")

    elif error_type == 'server_error':
        # Server-side issue
        log_error(f"Server error: {error_response.message}")
        schedule_retry(plan, delay=300)  # Retry in 5 minutes

    else:
        # Unknown error
        log_error(f"Unknown error: {error_response}")
        update_plan_status(plan, "Failed - Unknown Error")
```

## Integration with Silver Tier

### Input Sources
- Approval Manager → Approved plans ready for execution
- Task Processor → Triggers orchestration
- Scheduler Loop → Continuous monitoring

### Processing Flow

```
Approved plan in execution queue
    ↓
MCP Orchestrator picks up plan
    ↓
Parse plan steps
    ↓
For each step requiring MCP:
    ├─→ Validate approval still valid
    ├─→ Check server availability
    ├─→ Execute via MCP server
    ├─→ Log result
    └─→ Update plan progress
    ↓
All steps completed successfully
    ↓
Update plan: Status = Completed
    ↓
Move to Done folder
    ↓
Log completion with metrics
```

## Monitoring

### Health Check

```bash
# Check MCP server status
python -c "from mcp_orchestrator import check_all_servers; check_all_servers()"

# Check recent MCP calls
tail -20 logs/mcp_actions.log

# Check failed executions
grep "Failed" logs/mcp_actions.log
```

### Performance Metrics

- MCP calls per day (by server)
- Average execution time per action type
- Success rate by server
- Error rate and types
- Retry frequency
- Queue depth (pending executions)

### Alerts

**Critical**
- MCP server down
- Authentication failures
- Multiple consecutive failures

**Warning**
- High retry rate
- Slow response times
- Queue backlog growing

## Security

### Authentication

```python
def authenticate_mcp_call(server, action, plan):
    """
    Ensures MCP call is authorized.
    """
    # Verify plan is approved
    if not plan.is_approved():
        raise SecurityError("Plan not approved")

    # Verify approval hasn't expired
    if plan.approval_expired():
        raise SecurityError("Approval expired")

    # Verify action matches approved plan
    if action not in plan.approved_actions:
        raise SecurityError("Action not in approved plan")

    # Verify caller identity
    if not verify_caller_identity():
        raise SecurityError("Caller identity verification failed")

    return True
```

### Audit Trail

All MCP calls logged with:
- Timestamp
- Server and action
- Parameters (sanitized)
- Response status
- Execution time
- Plan ID and approver
- Result

```
[2026-02-16 14:20:30] [MCP_ORCHESTRATOR] CALL - Server: email-server, Action: send_email
[2026-02-16 14:20:30] [MCP_ORCHESTRATOR] PARAMS - To: client@***.com, Subject: Q4 Proposal
[2026-02-16 14:20:35] [MCP_ORCHESTRATOR] RESPONSE - Status: success, Time: 5.2s
[2026-02-16 14:20:35] [MCP_ORCHESTRATOR] AUDIT - Plan: 20260216-141530-Plan, Approver: user@company.com
```

## Testing

### Unit Tests

```python
# test_mcp_orchestrator.py

def test_action_parsing():
    plan = create_test_plan(steps=["Send email to client"])
    actions = parse_plan_actions(plan)
    assert actions[0]['action_type'] == 'send_email'
    assert actions[0]['server'] == 'email-server'

def test_server_mapping():
    action = 'post_linkedin'
    server = ACTION_TO_SERVER[action]
    assert server == 'linkedin-server'

def test_error_handling():
    error_response = {'status': 'error', 'error_type': 'rate_limit'}
    result = handle_mcp_error(error_response, test_plan, test_step)
    assert result.retry_scheduled == True
```

### Integration Tests

```bash
# Test full execution flow
python test_mcp_integration.py

# Test specific server
python test_mcp_server.py --server email-server

# Test error scenarios
python test_mcp_errors.py
```

## Configuration

```python
# mcp_config.py

MCP_CONFIG = {
    'timeout': 30,  # seconds
    'max_retries': 3,
    'retry_delay': 2,  # seconds (exponential backoff)
    'parallel_execution': False,
    'health_check_interval': 60,  # seconds
    'log_parameters': True,
    'sanitize_logs': True  # Remove sensitive data
}
```

## Dependencies

```python
import json
import time
import logging
from pathlib import Path
from datetime import datetime
```

## Logs

**Location**: `logs/mcp_actions.log`

**Format**:
```
[2026-02-16 14:20:30] [MCP_ORCHESTRATOR] CALL - email-server.send_email
[2026-02-16 14:20:35] [MCP_ORCHESTRATOR] SUCCESS - Message sent, ID: abc123
[2026-02-16 14:20:35] [MCP_ORCHESTRATOR] METRICS - Time: 5.2s, Retries: 0
```

## Future Enhancements

- [ ] GraphQL-based MCP protocol
- [ ] Async/await for parallel execution
- [ ] Circuit breaker pattern for failing servers
- [ ] Request queuing and prioritization
- [ ] Load balancing across server instances
- [ ] Real-time execution monitoring dashboard
- [ ] Integration with more MCP servers

## References

- MCP Protocol: https://modelcontextprotocol.io
- MCP Servers: `../../mcp_servers/`
- Task Processor: `../../AI_Employee_Vault/task_processor.py`
- Silver Architecture: `../docs/silver_architecture.md`
