# 🤖 Autonomous Social Media Posting System

## Playwright-Based Automation (Gold Tier)

Complete autonomous posting system using Playwright for LinkedIn, Twitter/X, and Facebook.

## 🚀 Setup (One Time)

### Step 1: Install Playwright
```powershell
.\setup_playwright.bat
```

This installs:
- Playwright library
- Chromium browser
- All dependencies

### Step 2: Add Credentials to .env

Edit your `.env` file:

```env
# LinkedIn (Already configured)
LINKEDIN_EMAIL=aishaanjumsiddiqui97@gmail.com
LINKEDIN_PASSWORD=Lara1997

# Twitter/X
TWITTER_EMAIL=your_email@gmail.com
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password

# Facebook
FACEBOOK_EMAIL=your_email@gmail.com
FACEBOOK_PASSWORD=your_password
```

### Step 3: Test Individual Platforms

```powershell
# Test LinkedIn
python playwright_linkedin.py

# Test Twitter
python playwright_twitter.py

# Test Facebook
python playwright_facebook.py
```

## 🎯 Autonomous Operation

### Start Autonomous Poster
```powershell
.\start_autonomous_poster.bat
```

This will:
- ✅ Monitor `03_Posted/History/` folder every 15 minutes
- ✅ Detect new approved posts
- ✅ Auto-post to respective platforms
- ✅ Rename files with `POSTED_` prefix
- ✅ Log errors to `System_Errors.md`
- ✅ Create alerts in `00_Inbox/ALERTS.md`

## 📋 Complete Workflow

### 1. Content Generation (Automatic)
Agent generates posts every 6 hours:
```
02_Pending_Approvals/Social_Posts/
├── LinkedIn_Post_20260225_120000.md
├── Twitter_Post_20260225_120000.md
└── Facebook_Post_20260225_120000.md
```

### 2. Approval (Manual - 5 seconds)
Move approved posts:
```powershell
move "02_Pending_Approvals\Social_Posts\*.md" "03_Posted\History\"
```

### 3. Auto-Posting (Automatic)
Autonomous poster detects and posts:
```
03_Posted/History/
├── POSTED_LinkedIn_Post_20260225_120000.md
├── POSTED_Twitter_Post_20260225_120000.md
└── POSTED_Facebook_Post_20260225_120000.md
```

## 🔄 The Ralph Wiggum Loop

```
┌─────────────────────────────────────────┐
│  Every 15 minutes:                      │
│                                         │
│  1. Scan 03_Posted/History/             │
│  2. Find non-POSTED_ files              │
│  3. Extract platform from filename      │
│  4. Launch headless browser             │
│  5. Login to platform                   │
│  6. Post content                        │
│  7. Rename file with POSTED_ prefix     │
│  8. Log success/failure                 │
│  9. Repeat                              │
└─────────────────────────────────────────┘
```

## 🎛️ Platform-Specific Details

### LinkedIn
- **Script**: `playwright_linkedin.py`
- **Credentials**: `LINKEDIN_EMAIL`, `LINKEDIN_PASSWORD`
- **Features**:
  - Multiple selector strategies
  - Screenshot on error
  - Headless mode support

### Twitter/X
- **Script**: `playwright_twitter.py`
- **Credentials**: `TWITTER_EMAIL`, `TWITTER_USERNAME`, `TWITTER_PASSWORD`
- **Features**:
  - 280 character limit auto-truncation
  - Email verification handling
  - Error screenshots

### Facebook
- **Script**: `playwright_facebook.py`
- **Credentials**: `FACEBOOK_EMAIL`, `FACEBOOK_PASSWORD`
- **Features**:
  - Multiple selector fallbacks
  - Error handling
  - Screenshot debugging

## 🛡️ Error Handling

### Automatic Error Recovery
- Login failures → Logged to `System_Errors.md`
- Post button not found → Screenshot saved
- Network issues → Retry next iteration
- Platform changes → Alert created

### Error Logs
```
System_Errors.md
├── Login failures
├── Posting errors
├── Network issues
└── Platform changes
```

### Alerts
```
00_Inbox/ALERTS.md
├── Critical failures
├── Platform issues
└── Manual intervention needed
```

## 📊 Monitoring

### Check Status
```powershell
# View error log
type System_Errors.md

# View alerts
type 00_Inbox\ALERTS.md

# Check posted files
dir 03_Posted\History\POSTED_*
```

### Activity Indicators
- ✅ Successfully posted
- ❌ Posting failed
- 🚨 Alert created
- 📸 Screenshot saved
- 🔄 Iteration complete

## ⚙️ Configuration

### Change Check Interval
Edit `autonomous_poster.py`:
```python
self.check_interval = 900  # 15 minutes (in seconds)
```

### Headless vs Visible Browser
Edit platform scripts:
```python
# Headless (background)
poster = LinkedInPosterPlaywright(headless=True)

# Visible (for debugging)
poster = LinkedInPosterPlaywright(headless=False)
```

### Add More Platforms
1. Create `playwright_instagram.py`
2. Add handler to `autonomous_poster.py`:
```python
self.platform_handlers = {
    'LinkedIn': post_to_linkedin,
    'Twitter': post_to_twitter,
    'Facebook': post_to_facebook,
    'Instagram': post_to_instagram  # New
}
```

## 🧪 Testing

### Test Single Platform
```powershell
# LinkedIn
python playwright_linkedin.py "03_Posted\History\LinkedIn_Post_XXXXX.md"

# Twitter
python playwright_twitter.py "03_Posted\History\Twitter_Post_XXXXX.md"

# Facebook
python playwright_facebook.py "03_Posted\History\Facebook_Post_XXXXX.md"
```

### Test Autonomous Loop (One Iteration)
```powershell
python -c "from autonomous_poster import AutonomousPoster; poster = AutonomousPoster(); poster.check_approved_posts()"
```

## 🎓 Best Practices

### 1. Test Before Going Live
- Test each platform individually
- Verify credentials work
- Check error handling

### 2. Monitor Regularly
- Check `System_Errors.md` daily
- Review `ALERTS.md` for issues
- Verify posts are going through

### 3. Keep Credentials Secure
- Never commit `.env` to git
- Use strong passwords
- Enable 2FA where possible

### 4. Handle Platform Changes
- Social media UIs change frequently
- Update selectors when needed
- Keep Playwright updated

## 🚨 Troubleshooting

### Playwright Not Installed
```powershell
.\setup_playwright.bat
```

### Login Fails
- Check credentials in `.env`
- Try manual login first
- Handle 2FA if enabled
- Check for CAPTCHA

### Post Button Not Found
- Platform UI may have changed
- Check error screenshots
- Update selectors in script
- Run in visible mode for debugging

### Browser Crashes
- Update Playwright: `pip install --upgrade playwright`
- Reinstall browsers: `python -m playwright install chromium`
- Check system resources

## 📈 Performance

### Resource Usage
- **CPU**: Low (headless mode)
- **Memory**: ~200MB per browser instance
- **Network**: Minimal (only during posting)

### Optimization
- Use headless mode for production
- Increase check interval if needed
- Close browsers after posting
- Monitor system resources

## ✅ Success Checklist

- [ ] Playwright installed
- [ ] Credentials in `.env`
- [ ] Individual platform tests pass
- [ ] Autonomous poster running
- [ ] Posts generating automatically
- [ ] Approval workflow working
- [ ] Auto-posting successful
- [ ] Error logging functional
- [ ] Alerts working

## 🎉 You're All Set!

Your autonomous posting system is now:
- ✅ Generating posts every 6 hours
- ✅ Waiting for your approval
- ✅ Auto-posting to all platforms
- ✅ Handling errors gracefully
- ✅ Running 24/7 autonomously

## 📚 Files Created

- `setup_playwright.bat` - Installation script
- `playwright_linkedin.py` - LinkedIn poster
- `playwright_twitter.py` - Twitter poster
- `playwright_facebook.py` - Facebook poster
- `autonomous_poster.py` - Main autonomous loop
- `start_autonomous_poster.bat` - Start script
- `AUTONOMOUS_POSTING_GUIDE.md` - This guide

## 🚀 Quick Start Commands

```powershell
# 1. Setup (one time)
.\setup_playwright.bat

# 2. Add credentials to .env

# 3. Test
python playwright_linkedin.py

# 4. Start autonomous mode
.\start_autonomous_poster.bat

# 5. Approve posts by moving to 03_Posted/History/

# 6. Watch it auto-post! 🎉
```

---

**The Ralph Wiggum Loop is now active with Playwright! 🤖**
