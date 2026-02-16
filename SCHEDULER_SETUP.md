# Windows Task Scheduler Setup Guide

## Automated Startup Configuration

### Step 1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc` and press Enter

### Step 2: Create New Task
1. Click "Create Task" (not "Create Basic Task")
2. Name: `Digital FTE - Auto Start`
3. Description: `Automatically starts all Digital FTE watchers`
4. Check "Run whether user is logged on or not"
5. Check "Run with highest privileges"

### Step 3: Triggers
1. Click "Triggers" tab → "New"
2. Begin the task: `At startup`
3. Delay task for: `30 seconds` (allows system to initialize)
4. Click OK

### Step 4: Actions
1. Click "Actions" tab → "New"
2. Action: `Start a program`
3. Program/script: `cmd.exe`
4. Add arguments: `/c "E:\Python.py\Hackaton 0\start_all_watchers.bat"`
5. Start in: `E:\Python.py\Hackaton 0`
6. Click OK

### Step 5: Conditions
1. Click "Conditions" tab
2. Uncheck "Start the task only if the computer is on AC power"
3. Click OK

### Step 6: Settings
1. Click "Settings" tab
2. Check "Allow task to be run on demand"
3. Check "If the task fails, restart every: 1 minute"
4. Attempt to restart up to: 3 times
5. Click OK

### Step 7: Test
Right-click the task → "Run" to test immediately

---

## Alternative: Manual Startup

Simply double-click `start_all_watchers.bat` when you want to start the system.

---

## Verification

Check that all 4 windows open:
- Vault Watcher
- Gmail Watcher
- LinkedIn Watcher
- WhatsApp Watcher

Check logs in `logs/` folder to verify activity.
