# Vault Watcher Server (MCP)

## Purpose
MCP server that provides read/write access to the Obsidian vault and monitors file system changes.

## Type
**MCP Server** - Vault integration and monitoring

## Risk Level
**Low-Medium** - Read operations are low risk, write operations are medium risk

## Implementation
**Location**: `../../../mcp_servers/vault_watcher_server.py`

## Capabilities

### Tools Provided

**read_vault_file**
- Reads any file from the vault
- Returns file content and metadata
- No approval required (read-only)

**Parameters**:
```json
{
  "file_path": "AI_Employee_Vault/Dashboard.md",
  "include_metadata": true
}
```

**Response**:
```json
{
  "status": "success",
  "content": "# Dashboard\n\n...",
  "metadata": {
    "created": "2026-02-10T10:00:00Z",
    "modified": "2026-02-16T14:20:00Z",
    "size": 1024,
    "path": "AI_Employee_Vault/Dashboard.md"
  }
}
```

**write_vault_file**
- Writes content to vault file
- Creates new file or updates existing
- Requires approval for sensitive locations

**Parameters**:
```json
{
  "file_path": "AI_Employee_Vault/Done/task_completed.md",
  "content": "# Task Completed\n\n...",
  "create_if_missing": true
}
```

**Response**:
```json
{
  "status": "success",
  "file_path": "AI_Employee_Vault/Done/task_completed.md",
  "action": "created",
  "timestamp": "2026-02-16T14:20:35Z"
}
```

**list_vault_files**
- Lists files in vault directory
- Supports filtering by pattern
- Returns file metadata

**Parameters**:
```json
{
  "directory": "AI_Employee_Vault/Inbox",
  "pattern": "*.md",
  "recursive": false
}
```

**Response**:
```json
{
  "status": "success",
  "files": [
    {
      "name": "task1.md",
      "path": "AI_Employee_Vault/Inbox/task1.md",
      "size": 512,
      "modified": "2026-02-16T10:30:00Z"
    }
  ],
  "count": 1
}
```

**move_vault_file**
- Moves file within vault
- Used for task workflow (Inbox → Plans → Done)
- Logs all moves for audit

**Parameters**:
```json
{
  "source": "AI_Employee_Vault/Inbox/task.md",
  "destination": "AI_Employee_Vault/Plans/task.md",
  "overwrite": false
}
```

**Response**:
```json
{
  "status": "success",
  "moved_from": "AI_Employee_Vault/Inbox/task.md",
  "moved_to": "AI_Employee_Vault/Plans/task.md",
  "timestamp": "2026-02-16T14:20:35Z"
}
```

**watch_directory**
- Monitors directory for changes
- Returns events (created, modified, deleted)
- Real-time file system monitoring

**Parameters**:
```json
{
  "directory": "AI_Employee_Vault/Inbox",
  "event_types": ["created", "modified"],
  "timeout": 60
}
```

**Response**:
```json
{
  "status": "success",
  "events": [
    {
      "type": "created",
      "path": "AI_Employee_Vault/Inbox/new_task.md",
      "timestamp": "2026-02-16T14:20:35Z"
    }
  ]
}
```

## Vault Structure

### Protected Directories

**Read-Only** (no approval needed):
- `AI_Employee_Vault/Done/` - Completed tasks
- `AI_Employee_Vault/Skills/` - Agent skill definitions
- `AI_Employee_Vault/Logs/` - System logs

**Read-Write** (low risk):
- `AI_Employee_Vault/Inbox/` - New tasks
- `AI_Employee_Vault/Plans/` - Generated plans
- `AI_Employee_Vault/Done/` - Completed tasks

**Restricted** (requires approval):
- `AI_Employee_Vault/Needs_Action/` - Pending approvals
- `AI_Employee_Vault/Company_Handbook.md` - Core documentation
- `AI_Employee_Vault/Dashboard.md` - System dashboard

## File System Monitoring

### Watchdog Integration

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VaultWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            log_event(f"New file created: {event.src_path}")
            trigger_processing(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            log_event(f"File modified: {event.src_path}")
            check_approval_status(event.src_path)
```

### Event Types

**Created**
- New task file in Inbox
- New plan in Plans or Needs_Action
- New log entry

**Modified**
- Approval status changed
- Plan updated
- Task content edited

**Deleted**
- File removed (logged for audit)
- Cleanup operations

**Moved**
- Task workflow progression
- File organization

## Integration with Silver Tier

### Task Workflow

```
File created in Inbox
    ↓
Vault Watcher detects event
    ↓
Triggers Reasoning Engine
    ↓
Plan generated and saved
    ↓
Vault Watcher detects new plan
    ↓
Routes based on risk level
    ↓
Monitors for approval changes
    ↓
Detects "Approved" status
    ↓
Triggers execution
    ↓
Moves completed task to Done
```

### Real-Time Monitoring

The Vault Watcher provides real-time file system monitoring that enables:
- Immediate task detection
- Approval status changes
- Plan updates
- Task completion tracking

## Configuration

### Watched Directories

```python
WATCHED_DIRECTORIES = [
    'AI_Employee_Vault/Inbox',
    'AI_Employee_Vault/Needs_Action',
    'AI_Employee_Vault/Plans'
]

WATCH_PATTERNS = ['*.md']
IGNORE_PATTERNS = ['.gitkeep', '*.tmp', '*~']
```

### Event Handling

```python
EVENT_HANDLERS = {
    'created': handle_file_created,
    'modified': handle_file_modified,
    'deleted': handle_file_deleted,
    'moved': handle_file_moved
}

DEBOUNCE_DELAY = 1  # seconds (prevent duplicate events)
```

## Logging

All vault operations logged to:
- `logs/vault_actions.log` - Detailed operation log

**Log Format**:
```
[2026-02-16 10:30:45] [VAULT_WATCHER] EVENT - File created: AI_Employee_Vault/Inbox/task.md
[2026-02-16 10:30:46] [VAULT_WATCHER] ACTION - Triggering reasoning engine
[2026-02-16 10:30:50] [VAULT_WATCHER] EVENT - File created: AI_Employee_Vault/Plans/20260216-103050-Plan.md
[2026-02-16 10:30:51] [VAULT_WATCHER] ACTION - Plan detected, monitoring for approval
```

## Error Handling

### Common Errors

**File Not Found**
```json
{
  "status": "error",
  "error_type": "not_found",
  "message": "File does not exist: AI_Employee_Vault/missing.md"
}
```

**Permission Denied**
```json
{
  "status": "error",
  "error_type": "permission",
  "message": "Cannot write to protected file without approval"
}
```

**Invalid Path**
```json
{
  "status": "error",
  "error_type": "validation",
  "message": "Path must be within AI_Employee_Vault directory"
}
```

## Security Features

- **Path Validation**: All paths must be within vault
- **Approval Required**: Sensitive files require approval
- **Audit Trail**: All operations logged
- **Read-Only Mode**: Can be configured for read-only access
- **Backup**: Automatic backup before destructive operations

## Usage Example

### From Claude Desktop

```
User: Show me what's in my Inbox

Claude: Let me check your Inbox...

[Calls vault-watcher MCP]

Claude: You have 3 tasks in your Inbox:

1. task1.md - Created 10:30 AM
2. task2.md - Created 11:15 AM
3. task3.md - Created 2:45 PM

Would you like me to read any of these?
```

### From Python

```python
from mcp_servers.vault_watcher_server import read_vault_file, list_vault_files

# List files in Inbox
result = list_vault_files(
    directory="AI_Employee_Vault/Inbox",
    pattern="*.md"
)

print(f"Found {result['count']} files")

# Read a specific file
content = read_vault_file("AI_Employee_Vault/Inbox/task1.md")
print(content['content'])
```

## Testing

### Manual Test

```bash
# Test file reading
python -c "
from mcp_servers.vault_watcher_server import read_vault_file
result = read_vault_file('AI_Employee_Vault/Dashboard.md')
print(result['content'][:100])
"

# Test file listing
python -c "
from mcp_servers.vault_watcher_server import list_vault_files
result = list_vault_files('AI_Employee_Vault/Inbox')
print(f'Found {result[\"count\"]} files')
"

# Test monitoring
python mcp_servers/vault_watcher_server.py --watch
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vault-watcher": {
      "command": "python",
      "args": ["E:\\Python.py\\Hackaton 0\\mcp_servers\\vault_watcher_server.py"]
    }
  }
}
```

## Dependencies

```
watchdog>=4.0.0  # File system monitoring
pathlib (built-in)
os (built-in)
```

## Performance

### Optimization

- **Event Debouncing**: Prevents duplicate events
- **Selective Monitoring**: Only watches relevant directories
- **Efficient Polling**: Minimal CPU usage
- **Async Operations**: Non-blocking file operations

### Resource Usage

- **CPU**: <1% (idle), ~5% (active monitoring)
- **Memory**: ~20MB
- **Disk I/O**: Minimal (event-driven)

## Backup & Recovery

### Automatic Backup

```python
def backup_before_write(file_path):
    """Create backup before modifying file."""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup.{int(time.time())}"
        shutil.copy2(file_path, backup_path)
        log_event(f"Backup created: {backup_path}")
```

### Recovery

```bash
# List backups
ls AI_Employee_Vault/**/*.backup.*

# Restore from backup
cp AI_Employee_Vault/file.md.backup.1234567890 AI_Employee_Vault/file.md
```

## Future Enhancements

- [ ] Git integration for version control
- [ ] Conflict resolution for concurrent edits
- [ ] File compression for large vaults
- [ ] Cloud sync integration
- [ ] Advanced search capabilities
- [ ] File templates
- [ ] Bulk operations

## References

- Implementation: `../../../mcp_servers/vault_watcher_server.py`
- Bronze Watcher: `../../../AI_Employee_Vault/watcher.py`
- Watchdog Documentation: https://python-watchdog.readthedocs.io/
- MCP Protocol: https://modelcontextprotocol.io
