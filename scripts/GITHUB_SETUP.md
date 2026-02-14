# GitHub Watcher Setup Guide

## Overview
GitHub Watcher monitors your GitHub repository for new issues, pull requests, and push events, automatically creating tasks and triggering AI processing.

---

## Prerequisites

1. **GitHub Account** with access to the repository you want to monitor
2. **GitHub Personal Access Token** with appropriate permissions
3. **Repository Name** in format: `owner/repo-name`

---

## Setup Instructions

### Step 1: Create GitHub Personal Access Token

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Give it a descriptive name: "GitHub Watcher"

3. **Select Scopes**
   - ✅ `repo` - Full control of private repositories
   - ✅ `notifications` - Access notifications
   - ✅ `read:org` - Read org and team membership (if monitoring org repos)

4. **Generate and Copy Token**
   - Click "Generate token"
   - **IMPORTANT:** Copy the token immediately (you won't see it again)

### Step 2: Configure GitHub Watcher

1. **Edit configuration file:**
   ```
   AI_Employee_Vault/scripts/github_config.json
   ```

2. **Update settings:**
   ```json
   {
     "repository": "your-username/your-repo-name",
     "github_token": "ghp_your_token_here",
     "monitored_events": [
       "issues",
       "pull_requests",
       "pushes"
     ],
     "settings": {
       "check_interval_seconds": 60,
       "create_tasks": true,
       "trigger_ai_processing": true
     }
   }
   ```

3. **Replace:**
   - `your-username/your-repo-name` with your actual repository
   - `ghp_your_token_here` with your GitHub token

### Step 3: Test the Watcher

**Run manually to test:**
```bash
python scripts/github_watcher.py
```

**Expected output:**
```
[2026-02-12 23:30:00] GITHUB WATCHER STARTED
[2026-02-12 23:30:00] Monitoring repository: owner/repo
[2026-02-12 23:30:00] Monitored events: issues, pull_requests, pushes
[2026-02-12 23:30:00] Loaded 0 previously processed event IDs
[2026-02-12 23:30:01] Found 30 recent event(s)
```

---

## Monitored Events

### Issues
- New issues created
- Issues opened, closed, or reopened
- Creates task with issue details and action items

### Pull Requests
- New PRs created
- PRs opened, closed, merged, or reopened
- Creates task with PR details and review checklist

### Push Events
- New commits pushed to repository
- Creates task with commit messages and branch info

---

## Task Creation

When an event is detected, GitHub Watcher:

1. **Creates a task file** in `AI_Employee_Vault/Needs_Action/`
2. **Formats based on event type:**
   - Issues: `GitHub_Issue_123_20260212_233000.md`
   - PRs: `GitHub_PR_456_20260212_233000.md`
   - Pushes: `GitHub_Push_20260212_233000.md`

3. **Triggers task processor** to handle the task
4. **Moves to Done/** when processed
5. **Logs in System_Log.md**

---

## Configuration Options

### Monitored Events

Enable/disable specific event types:
```json
"monitored_events": [
  "issues",           // Monitor issue events
  "pull_requests",    // Monitor PR events
  "pushes"           // Monitor push events
]
```

### Check Interval

Adjust polling frequency (in seconds):
```json
"check_interval_seconds": 60  // Check every 60 seconds
```

**Note:** GitHub API has rate limits:
- Authenticated: 5,000 requests/hour
- At 60-second intervals: ~60 requests/hour (well within limits)

---

## Running as Service

### Option 1: Run Manually
```bash
python scripts/github_watcher.py
```

### Option 2: Run in Background (Windows)
```bash
start /B python scripts/github_watcher.py
```

### Option 3: Task Scheduler (Recommended)

Create a scheduled task similar to Gmail Watcher:

1. **Create batch file:** `scripts/start_github_watcher.bat`
   ```batch
   @echo off
   cd /d "%~dp0.."
   AI_Employee_Vault\venv\Scripts\python.exe scripts\github_watcher.py
   ```

2. **Use Task Scheduler** to run at startup

---

## Logs

### Main Log
```
logs/actions.log
```

Contains all GitHub Watcher activity:
```
[2026-02-12 23:30:00] GITHUB WATCHER STARTED
[2026-02-12 23:30:01] GITHUB_EVENT - IssuesEvent by username
[2026-02-12 23:30:01] TASK_CREATED - GitHub_Issue_123_20260212_233001.md
[2026-02-12 23:30:01] TRIGGERING_PROCESSOR - GitHub_Issue_123_20260212_233001.md
[2026-02-12 23:30:02] PROCESSOR_SUCCESS - GitHub_Issue_123_20260212_233001.md
```

### Processed Events
```
logs/processed_github_events.txt
```

Tracks processed event IDs to prevent duplicates.

---

## Troubleshooting

### Authentication Failed

**Error:** `GitHub authentication failed. Check your token.`

**Solution:**
1. Verify token is correct in `github_config.json`
2. Check token hasn't expired
3. Ensure token has correct scopes (`repo`)

### Repository Not Found

**Error:** `Repository 'owner/repo' not found`

**Solution:**
1. Verify repository name format: `owner/repo-name`
2. Check you have access to the repository
3. For private repos, ensure token has `repo` scope

### Rate Limit Exceeded

**Error:** `GitHub API rate limit exceeded`

**Solution:**
1. Increase `check_interval_seconds` in config
2. Check you're using authenticated requests (token configured)
3. Wait for rate limit to reset (shown in error message)

### No Events Detected

**Possible causes:**
1. Repository has no recent activity
2. Event types not in `monitored_events` list
3. All events already processed (check `processed_github_events.txt`)

**Solution:**
- Clear `logs/processed_github_events.txt` to reprocess events
- Verify repository has recent activity
- Check monitored event types match repository activity

---

## Security Notes

- **Never commit** `github_config.json` with your token
- Add to `.gitignore`:
  ```
  AI_Employee_Vault/scripts/github_config.json
  ```
- Tokens should be treated like passwords
- Regenerate token if compromised
- Use minimum required scopes

---

## Integration with Gmail Watcher

Both watchers can run simultaneously:

**Gmail Watcher:** Monitors email (every 30 seconds)
**GitHub Watcher:** Monitors repository (every 60 seconds)

Both create tasks in the same `Needs_Action/` folder and use the same task processor.

---

## Example Task Output

### Issue Task
```markdown
# 🐛 GitHub Issue: Bug in login form

## Issue Details
- **Repository:** owner/repo
- **Issue #:** 123
- **Action:** opened
- **Created by:** username
- **Date:** 2026-02-12T23:30:00Z
- **URL:** https://github.com/owner/repo/issues/123

## Description
The login form doesn't validate email addresses properly...

## Action Items
- [ ] Review the issue
- [ ] Assign if needed
- [ ] Respond or take action
```

---

## API Rate Limits

GitHub API limits:
- **Authenticated:** 5,000 requests/hour
- **Unauthenticated:** 60 requests/hour

With 60-second intervals:
- **Requests per hour:** ~60
- **Well within limits:** ✅

---

## Support

If you encounter issues:
1. Check logs: `logs/actions.log`
2. Verify token and repository configuration
3. Test GitHub API access manually
4. Ensure internet connection is stable
