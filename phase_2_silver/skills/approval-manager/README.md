# Approval Manager Skill

## Purpose
Manages the human-in-the-loop approval workflow for medium and high-risk tasks, ensuring critical operations require explicit human authorization.

## Type
**Control Skill** - Approval workflow orchestrator

## Risk Level
**Low** - Monitoring only, no autonomous actions

## Implementation
**Location**: Integrated into `../../AI_Employee_Vault/reasoning_engine.py` and `../../AI_Employee_Vault/task_processor.py`

## Functionality

### What It Does
1. Monitors `AI_Employee_Vault/Needs_Action/` for plans requiring approval
2. Detects when human updates `Approval Status` field
3. Validates approval format and authenticity
4. Routes approved plans to execution queue
5. Handles rejected plans appropriately
6. Manages approval timeouts
7. Logs all approval decisions
8. Notifies relevant parties of status changes

### Approval Workflow States

```
Plan Created (Risk: Medium/High)
    ↓
Moved to /Needs_Action
    ↓
Approval Status: Pending
    ↓
Human Reviews Plan
    ↓
    ├─→ Approval Status: Approved → Execute via MCP
    ├─→ Approval Status: Rejected → Move to Done with rejection note
    └─→ No action for 24h → Approval Status: Expired → Move to Done
```

## Approval Status Values

### Valid Statuses

**Pending**
- Initial state for all medium/high risk plans
- Waiting for human review
- No action taken yet

**Approved**
- Human has reviewed and authorized execution
- Plan moves to execution queue
- MCP Orchestrator takes over

**Rejected**
- Human has declined to authorize
- Plan moved to Done with rejection reason
- No execution occurs

**Expired**
- No human response within timeout period (default: 24 hours)
- Plan moved to Done with expiration note
- Requires manual re-submission if still needed

**Clarification Needed**
- Human requests more information
- Plan remains in Needs_Action
- Additional context added to plan

## Approval Validation

### Format Requirements

Plans must have exact text match for approval:

```markdown
**Approval Status**: Approved
```

**Invalid formats** (will be ignored):
- `Approval Status: approved` (lowercase)
- `Status: Approved` (wrong field name)
- `Approval: Yes` (wrong format)
- `APPROVED` (missing field structure)

### Validation Logic

```python
def validate_approval(plan_path):
    """
    Validates that a plan has proper approval.
    Returns (is_valid, message)
    """
    try:
        content = plan_path.read_text(encoding='utf-8')
        content_lower = content.lower()

        # Check for required fields
        required_fields = ['goal:', 'risk level:', 'approval status:']
        if not all(field in content_lower for field in required_fields):
            return False, "Missing required plan fields"

        # Check risk level
        risk_level = extract_field(content, 'Risk Level')

        # Low risk doesn't need approval
        if risk_level == "Low":
            return True, "Low risk - auto-approved"

        # Medium/High risk requires explicit approval
        if risk_level in ["Medium", "High"]:
            if "approval status: approved" not in content_lower:
                return False, f"{risk_level} risk requires explicit approval"

        return True, "Approval validated"

    except Exception as e:
        return False, f"Validation error: {e}"
```

## Integration with Silver Tier

### Input Sources
- Plan Generator → Creates plans in /Needs_Action
- Human User → Updates Approval Status field
- Timeout Monitor → Detects expired approvals

### Processing Flow

```
Plan in /Needs_Action (Approval Status: Pending)
    ↓
Approval Manager monitors file
    ↓
Detects file modification
    ↓
Reads Approval Status field
    ↓
    ├─→ "Approved" → Validate → Route to MCP Orchestrator
    ├─→ "Rejected" → Log reason → Move to Done
    ├─→ "Clarification Needed" → Notify user → Keep in Needs_Action
    └─→ Still "Pending" → Check timeout → Expire if needed
```

### Output Actions

**On Approval**
1. Validate approval format
2. Log approval decision
3. Add execution metadata to plan
4. Move plan to execution queue
5. Notify MCP Orchestrator
6. Update system log

**On Rejection**
1. Log rejection reason (if provided)
2. Add rejection timestamp
3. Move plan to Done folder
4. Update system log
5. Notify user (optional)

**On Expiration**
1. Check if timeout exceeded (default: 24h)
2. Add expiration note to plan
3. Move to Done folder
4. Log expiration event
5. Notify user of expired approval

## Approval Policies

### Risk-Based Policies

**Low Risk** (Auto-approved)
- No human approval needed
- Logged for audit trail
- Immediate execution

**Medium Risk** (Standard approval)
- Requires single human approval
- 24-hour timeout
- Can be delegated to authorized users

**High Risk** (Strict approval)
- Requires explicit approval
- May require dual approval (configurable)
- Shorter timeout (12 hours)
- Additional verification steps

### Configurable Policies

```python
# approval_policies.py

APPROVAL_POLICIES = {
    'Low': {
        'requires_approval': False,
        'auto_approve': True,
        'timeout_hours': None
    },
    'Medium': {
        'requires_approval': True,
        'auto_approve': False,
        'timeout_hours': 24,
        'dual_approval': False
    },
    'High': {
        'requires_approval': True,
        'auto_approve': False,
        'timeout_hours': 12,
        'dual_approval': True,  # Requires two approvers
        'authorized_approvers': ['manager@company.com']
    }
}
```

## Notification System

### Approval Requests

When a plan requires approval:

```markdown
# Approval Request Notification

**Plan**: Send Proposal to Client
**Risk Level**: Medium
**Created**: 2026-02-16 14:15:30
**Timeout**: 2026-02-17 14:15:30 (24 hours)

**Action Required**: Review plan in Needs_Action folder

**Location**: AI_Employee_Vault/Needs_Action/20260216-141530-Plan.md

**Quick Actions**:
- To approve: Change "Approval Status: Pending" to "Approval Status: Approved"
- To reject: Change to "Approval Status: Rejected" and add reason
- To request clarification: Change to "Approval Status: Clarification Needed" and add questions
```

### Notification Channels

1. **System Log** - Always logged
2. **Desktop Notification** - Optional (using plyer)
3. **Email** - Optional (for high-risk items)
4. **Dashboard Update** - Updates Dashboard.md with pending count

## Audit Trail

### Approval Logging

All approval decisions logged to `logs/approvals.log`:

```
[2026-02-16 14:15:30] [APPROVAL_MANAGER] REQUEST - Plan: 20260216-141530-Plan.md, Risk: Medium
[2026-02-16 14:20:15] [APPROVAL_MANAGER] APPROVED - Plan: 20260216-141530-Plan.md, Approver: user@company.com
[2026-02-16 14:20:16] [APPROVAL_MANAGER] ROUTED - Plan sent to MCP Orchestrator for execution
```

### Approval History

Maintain approval history in plan file:

```markdown
## Approval History

**Requested**: 2026-02-16 14:15:30
**Reviewed**: 2026-02-16 14:20:15
**Decision**: Approved
**Approver**: user@company.com
**Notes**: Proposal reviewed and looks good. Client email verified.
```

## Security & Compliance

### Authorization

```python
def is_authorized_approver(user, risk_level):
    """
    Checks if user is authorized to approve plans at given risk level.
    """
    if risk_level == "Low":
        return True  # Auto-approved

    if risk_level == "Medium":
        # Any authenticated user can approve medium risk
        return user in AUTHORIZED_USERS

    if risk_level == "High":
        # Only managers can approve high risk
        return user in AUTHORIZED_MANAGERS
```

### Audit Requirements

- All approvals logged with timestamp
- Approver identity recorded
- Rejection reasons documented
- Timeout events tracked
- Changes to approval status logged

### Compliance Features

- **SOX Compliance**: Separation of duties (creator ≠ approver)
- **GDPR**: Data handling approvals documented
- **ISO 27001**: Access control and audit trail
- **HIPAA**: Sensitive data handling approvals

## Monitoring

### Health Check

```bash
# Check pending approvals
ls -la AI_Employee_Vault/Needs_Action/ | grep Plan

# Check approval log
tail -20 logs/approvals.log

# Count pending by risk level
grep "Risk Level: High" AI_Employee_Vault/Needs_Action/*.md | wc -l
```

### Performance Metrics

- Average approval time (request to decision)
- Approval rate (approved vs rejected)
- Timeout rate (expired approvals)
- Approvals by risk level
- Approvals by approver

### Alerts

**Critical Alerts**
- High-risk plan pending > 6 hours
- Multiple rejections of same plan type
- Unusual approval patterns

**Warning Alerts**
- Medium-risk plan pending > 12 hours
- Approval backlog > 10 items
- Frequent timeouts

## Error Handling

### Common Issues

**Invalid Approval Format**
- Log warning with correct format
- Keep plan in Needs_Action
- Notify user of format error

**Concurrent Modifications**
- Detect file conflicts
- Use file locking if needed
- Retry with exponential backoff

**Missing Approver Information**
- Default to system user
- Log anonymous approval
- Flag for review

## Testing

### Unit Tests

```python
# test_approval_manager.py

def test_approval_validation():
    plan = create_test_plan(risk="Medium", status="Approved")
    is_valid, msg = validate_approval(plan)
    assert is_valid == True

def test_rejection_handling():
    plan = create_test_plan(risk="High", status="Rejected")
    result = process_approval(plan)
    assert result.status == "rejected"
    assert plan.location == "Done"

def test_timeout_detection():
    plan = create_test_plan(created=24_hours_ago)
    is_expired = check_timeout(plan)
    assert is_expired == True
```

### Integration Tests

```bash
# Create test plan requiring approval
cat > AI_Employee_Vault/Needs_Action/test_approval.md << 'EOF'
# Plan: Test Approval

**Goal**: Test approval workflow

**Risk Level**: Medium
**Approval Required**: Yes
**Approval Status**: Pending
EOF

# Simulate approval
sed -i 's/Pending/Approved/' AI_Employee_Vault/Needs_Action/test_approval.md

# Wait for processing
sleep 5

# Verify plan moved to execution
ls AI_Employee_Vault/Plans/ | grep test_approval
```

## Configuration

### Timeout Settings

```python
# approval_config.py

TIMEOUT_SETTINGS = {
    'Medium': 24 * 3600,  # 24 hours in seconds
    'High': 12 * 3600,    # 12 hours in seconds
    'check_interval': 300  # Check every 5 minutes
}
```

### Notification Settings

```python
NOTIFICATION_SETTINGS = {
    'desktop_notifications': True,
    'email_notifications': False,
    'email_for_high_risk_only': True,
    'dashboard_updates': True
}
```

## Dependencies

```python
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
```

## Logs

**Location**: `logs/approvals.log`

**Format**:
```
[2026-02-16 14:15:30] [APPROVAL_MANAGER] REQUEST - Plan: 20260216-141530-Plan.md, Risk: Medium, Timeout: 24h
[2026-02-16 14:20:15] [APPROVAL_MANAGER] APPROVED - Plan: 20260216-141530-Plan.md, Time: 4m 45s
[2026-02-16 14:20:16] [APPROVAL_MANAGER] ROUTED - Plan sent to execution queue
```

## Future Enhancements

- [ ] Multi-level approval workflows
- [ ] Approval delegation
- [ ] Mobile app for approvals
- [ ] AI-assisted risk assessment
- [ ] Approval templates for common scenarios
- [ ] Integration with Slack/Teams for notifications
- [ ] Approval analytics dashboard

## References

- Reasoning Engine: `../../AI_Employee_Vault/reasoning_engine.py`
- Task Processor: `../../AI_Employee_Vault/task_processor.py`
- Silver Architecture: `../docs/silver_architecture.md`
