# GitHub Watcher Setup - Step by Step Guide

## Step 1: Find Your GitHub Username

1. Go to: https://github.com
2. Sign in with: aishaanjumsiddiqui97@gmail.com
3. Click your profile picture (top right)
4. Your username is shown there (NOT the email)
   - Example: If it shows "@aishaanjumsiddiqui97" - your username is "aishaanjumsiddiqui97"

## Step 2: Choose Repository to Monitor

List your repositories:
1. Go to: https://github.com/YOUR_USERNAME?tab=repositories
2. Choose which repository you want to monitor
3. Note the full name: YOUR_USERNAME/REPO_NAME

Example: aishaanjumsiddiqui97/my-project

## Step 3: Create GitHub Personal Access Token

1. **Go to Token Settings:**
   https://github.com/settings/tokens

2. **Click "Generate new token (classic)"**

3. **Fill in details:**
   - Note: "GitHub Watcher for Digital FTE"
   - Expiration: 90 days (or No expiration)

4. **Select scopes (IMPORTANT):**
   ✅ Check these boxes:
   - [x] repo (Full control of private repositories)
   - [x] notifications (Access notifications)

5. **Click "Generate token"**

6. **COPY THE TOKEN IMMEDIATELY**
   - It looks like: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   - You won't see it again!
   - Save it somewhere safe temporarily

## Step 4: Configure GitHub Watcher

Once you have:
- Your GitHub username
- Repository name (username/repo)
- Personal access token

Tell me these details and I'll configure the watcher for you!

---

## Quick Reference

**What I need from you:**
1. GitHub username: _____________
2. Repository to monitor: _____________/_____________
3. GitHub token: ghp_xxxxxxxxxxxxx

**Then I will:**
- Update the configuration file
- Test the connection
- Start the GitHub watcher
- Show you the results
