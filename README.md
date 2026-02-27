# 🏆 Digital FTE - AI Employee Automation System

[![Gold Tier](https://img.shields.io/badge/Tier-Gold-FFD700?style=for-the-badge)](https://github.com/Aishasiddiqui97/Hackaton-0)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.41-green?style=for-the-badge&logo=selenium)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

> **Fully autonomous AI employee system with LinkedIn posting, Odoo integration, and 24/7 operation**

## 🎯 Project Overview

A production-ready autonomous system that handles:
- ✅ **LinkedIn Posting** - Fully automated with anti-detection
- ✅ **Odoo Accounting** - Docker-based ERP integration
- ✅ **Social Media** - Multi-platform support
- ✅ **24/7 Operation** - Autonomous loop with error recovery
- ✅ **Unicode Safe** - Handles emoji and special characters

## 🚀 Quick Start

### Prerequisites
```bash
# Required
- Python 3.12+
- Chrome Browser
- Git

# Optional
- Docker (for Odoo)
- Node.js (for additional features)
```

### Installation

```bash
# Clone repository
git clone https://github.com/Aishasiddiqui97/Hackaton-0.git
cd Hackaton-0

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.template .env
# Edit .env with your credentials

# Test LinkedIn posting
.\post_now.bat

# Start autonomous system
.\start_fully_autonomous.bat
```

## 📋 Features

### 🤖 Gold Tier Features

#### 1. Fully Autonomous LinkedIn Posting
- **Anti-Detection**: Stealth mode with human-like behavior
- **Unicode Safe**: Handles emoji and special characters
- **Error Recovery**: Continues operation on failures
- **24/7 Operation**: Runs continuously with 6-hour intervals

```bash
# Instant post (test)
.\post_now.bat

# Autonomous 24/7
.\start_fully_autonomous.bat

# Test login only
.\test_login.bat
```

#### 2. Odoo Integration
- **Docker Setup**: Complete Odoo 17.0 with PostgreSQL
- **API Access**: XML-RPC integration
- **Accounting**: Invoice, customer, payment management

```bash
# Start Odoo
docker-compose up -d

# Access: http://localhost:8069
# Database: odoo
# User: admin / admin
```

#### 3. Multi-Platform Social Media
- LinkedIn (Fully Automated)
- Twitter/X (API Ready)
- Facebook (API Ready)
- Instagram (Text-to-Image)

### 🥈 Silver Tier Features

#### 1. Scheduled Operations
- Daily Odoo sync
- Weekly CEO briefings
- Automated reporting

```bash
# Setup scheduler
.\setup_silver_tier_scheduler.bat

# Verify setup
python verify_silver_tier.py
```

#### 2. Email Integration
- Gmail monitoring
- Auto-response system
- Email drafting

#### 3. WhatsApp Integration
- Message monitoring
- Auto-reply capability
- Urgent message handling

## 📁 Project Structure

```
Hackaton-0/
├── 📂 00_Inbox/              # Incoming tasks
├── 📂 01_Drafts/             # Auto-generated content
├── 📂 02_Pending_Approvals/  # Content awaiting approval
├── 📂 03_Posted/             # Published content history
├── 📂 AI_Employee_Vault/     # Core system files
│   ├── Architecture/         # System design docs
│   ├── CEO_Briefings/        # Executive reports
│   └── scripts/              # Automation scripts
├── 📂 config/                # Configuration files
├── 📄 linkedin_auto_poster.py        # LinkedIn automation
├── 📄 fully_autonomous_linkedin.py   # 24/7 autonomous system
├── 📄 odoo_integration_example.py    # Odoo API client
├── 📄 docker-compose.yml             # Odoo Docker setup
└── 📄 requirements.txt               # Python dependencies
```

## 🛠️ Configuration

### LinkedIn Credentials
Edit `.env` file:
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

### Odoo Configuration
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

### Social Media APIs
```env
# Twitter
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret

# Facebook
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_account_id
```

## 📊 System Architecture

### Autonomous Loop Flow
```
┌─────────────────────────────────────┐
│   Fully Autonomous System           │
├─────────────────────────────────────┤
│                                     │
│  1. Generate Post (Random Template) │
│           ↓                         │
│  2. Clean Unicode/Emoji             │
│           ↓                         │
│  3. Login to LinkedIn               │
│           ↓                         │
│  4. Post Content (JS Injection)     │
│           ↓                         │
│  5. Mark as Posted                  │
│           ↓                         │
│  6. Wait 6 Hours                    │
│           ↓                         │
│  7. Repeat (24/7)                   │
│                                     │
└─────────────────────────────────────┘
```

### Anti-Detection Features
- ✅ Hidden automation flags
- ✅ Real Chrome user agent
- ✅ Human-like typing (0.05-0.15s per char)
- ✅ Random delays between actions
- ✅ Natural scrolling behavior
- ✅ CDP commands for stealth

## 🔧 Advanced Usage

### Custom Post Templates
Edit `fully_autonomous_linkedin.py`:
```python
self.post_templates = [
    "Your custom post here #Hashtags",
    "Another post template #More #Tags",
    # Add more...
]
```

### Change Posting Interval
```python
self.post_interval = 21600  # 6 hours (in seconds)

# Options:
# 3 hours: 10800
# 12 hours: 43200
# 24 hours: 86400
```

### Headless Mode
```python
poster = LinkedInPoster(headless=True)  # No browser window
```

## 📈 Monitoring

### System Status
- `System_Live_Status.md` - Real-time status
- `System_Errors.md` - Error logs
- Screenshots saved on failures

### Check Posted Content
```bash
dir 03_Posted\History\POSTED_*.md
```

## 🐛 Troubleshooting

### Login Issues
```bash
# Test credentials
.\test_login.bat

# Check .env file
LINKEDIN_EMAIL=correct_email
LINKEDIN_PASSWORD=correct_password
```

### Unicode/Emoji Errors
✅ **Fixed!** System automatically cleans non-BMP characters

### Browser Not Opening
```bash
# Install/update Chrome
# Reinstall Selenium
pip install --upgrade selenium webdriver-manager
```

## 📚 Documentation

- **[AUTO_POST_GUIDE.md](AUTO_POST_GUIDE.md)** - Complete posting guide
- **[ANTI_DETECTION_FEATURES.md](ANTI_DETECTION_FEATURES.md)** - Stealth features
- **[ODOO_QUICK_START.md](ODOO_QUICK_START.md)** - Odoo setup guide
- **[SIMPLE_START.md](SIMPLE_START.md)** - Quick start guide
- **[LINKEDIN_API_GUIDE_URDU.md](LINKEDIN_API_GUIDE_URDU.md)** - Urdu/Hindi guide

## 🎓 Tier Progression

### Bronze Tier ✅
- Basic file monitoring
- Manual task processing
- Simple logging

### Silver Tier ✅
- Scheduled operations
- Email integration
- WhatsApp monitoring
- CEO briefings

### Gold Tier ✅ (Current)
- Fully autonomous LinkedIn posting
- Anti-detection features
- Unicode/emoji safe
- 24/7 operation
- Error recovery
- Odoo integration
- Multi-platform support

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Selenium WebDriver team
- LinkedIn for the platform
- Odoo community
- Python community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Aishasiddiqui97/Hackaton-0/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aishasiddiqui97/Hackaton-0/discussions)

## 🎯 Roadmap

- [ ] AI-generated post content
- [ ] Multi-account support
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Cloud deployment
- [ ] Advanced scheduling

## ⭐ Star History

If this project helped you, please star it! ⭐

---

**Made with ❤️ for automation enthusiasts**

**Repository**: https://github.com/Aishasiddiqui97/Hackaton-0
