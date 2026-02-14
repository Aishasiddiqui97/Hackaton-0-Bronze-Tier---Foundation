# Windows Service Setup Guide

## Overview
This guide will help you set up Gmail Watcher to run automatically as a Windows service using Task Scheduler.

---

## Prerequisites

1. **Administrator Access** - Required to create scheduled tasks
2. **Gmail Watcher Working** - Test manually first before installing as service
3. **Credentials Configured** - `credentials.json` and `token.json` must be set up

---

## Installation Methods

### Method 1: Task Scheduler (Recommended)

**Advantages:**
- Built into Windows
- Easy to manage
- Auto-restart on failure
- Runs at system startup

**Installation Steps:**

1. **Open PowerShell as Administrator**
   - Right-click PowerShell
   - Select "Run as Administrator"

2. **Navigate to project directory**
   ```powershell
   cd "E:\Python.py\Hackaton 0"
   ```

3. **Run installation script**
   ```powershell
   .\scripts\install_service.ps1
   ```

4. **Follow prompts**
   - Confirm installation
   - Choose to start now or later

5. **Verify installation**
   ```powershell
   .\scripts\manage_service.ps1 status
   ```

---

## Service Management

### Using PowerShell Scripts

**Check Status:**
```powershell
.\scripts\manage_service.ps1 status
```

**Start Service:**
```powershell
.\scripts\manage_service.ps1 start
```

**Stop Service:**
```powershell
.\scripts\manage_service.ps1 stop
```

**Restart Service:**
```powershell
.\scripts\manage_service.ps1 restart
```

**View Logs:**
```powershell
.\scripts\manage_service.ps1 logs
```

### Using Task Scheduler GUI

1. Open Task Scheduler (taskschd.msc)
2. Find "GmailWatcherService" in Task Scheduler Library
3. Right-click for options:
   - Run
   - End
   - Disable
   - Properties

---

## Uninstallation

**Run uninstall script:**
```powershell
.\scripts\uninstall_service.ps1
```

Or manually:
```powershell
Unregister-ScheduledTask -TaskName "GmailWatcherService" -Confirm:$false
```

---

## Troubleshooting

### Service Won't Start

**Check logs:**
```powershell
Get-Content logs\actions.log -Tail 50
```

**Verify paths:**
- Ensure `credentials.json` exists
- Ensure `token.json` exists
- Check virtual environment is intact

**Test manually:**
```powershell
AI_Employee_Vault\venv\Scripts\python.exe AI_Employee_Vault\scripts\gmail_watcher.py
```

### Service Stops Unexpectedly

**Check Task Scheduler history:**
1. Open Task Scheduler
2. Right-click "GmailWatcherService"
3. Select "Properties"
4. Go to "History" tab

**Enable detailed logging:**
- Check `logs\actions.log` for errors
- Look for Python errors or API issues

### Credentials Expired

If token expires:
1. Stop the service
2. Delete `token.json`
3. Run manually to re-authenticate
4. Restart the service

---

## Configuration

### Auto-Start on Boot

Already configured by default. To verify:
```powershell
Get-ScheduledTask -TaskName "GmailWatcherService" | Select-Object -ExpandProperty Triggers
```

### Restart on Failure

Configured to restart 3 times with 1-minute intervals.

To modify:
1. Open Task Scheduler
2. Right-click "GmailWatcherService" → Properties
3. Go to "Settings" tab
4. Adjust restart settings

---

## Advanced Configuration

### Change Check Interval

Edit `AI_Employee_Vault\scripts\gmail_watcher.py`:
```python
CHECK_INTERVAL = 30  # Change to desired seconds
```

### Run as Different User

1. Open Task Scheduler
2. Right-click "GmailWatcherService" → Properties
3. Go to "General" tab
4. Click "Change User or Group"
5. Select different user

---

## Monitoring

### View Real-Time Logs

**PowerShell:**
```powershell
Get-Content logs\actions.log -Wait -Tail 10
```

**Command Prompt:**
```cmd
tail -f logs\actions.log
```

### Check Service Health

```powershell
# Check if running
$task = Get-ScheduledTask -TaskName "GmailWatcherService"
$task.State

# Check last run result
$info = Get-ScheduledTaskInfo -TaskName "GmailWatcherService"
$info.LastTaskResult
```

---

## Security Notes

- Service runs as your user account
- Has access to your Gmail via OAuth2
- Credentials stored in `credentials.json` and `token.json`
- Add these to `.gitignore` to prevent commits

---

## Performance

- **Memory Usage:** ~50-100 MB
- **CPU Usage:** Minimal (only during email checks)
- **Network:** Minimal (API calls every 30 seconds)
- **Disk:** Log files grow over time (rotate recommended)

---

## Support

If you encounter issues:
1. Check logs: `logs\actions.log`
2. Test manually first
3. Verify credentials are valid
4. Check internet connection
5. Ensure Gmail API is enabled

---

## Files Created

- `scripts\install_service.ps1` - Installation script
- `scripts\uninstall_service.ps1` - Uninstallation script
- `scripts\manage_service.ps1` - Management script
- `scripts\start_gmail_watcher.bat` - Service launcher
- `scripts\SERVICE_SETUP.md` - This guide
