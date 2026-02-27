#!/usr/bin/env python3
"""
Gold Tier Autonomous System - Full Automation
Ralph Wiggum Loop Mode - Never Stops, Never Asks
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()

# Import all modules
try:
    from playwright_linkedin import post_to_linkedin
    LINKEDIN_AVAILABLE = True
except:
    LINKEDIN_AVAILABLE = False

try:
    from fix_twitter_oauth import post_tweet_oauth, extract_content as extract_twitter
    import tweepy
    TWITTER_AVAILABLE = True
except:
    TWITTER_AVAILABLE = False

try:
    from api_facebook_poster import post_to_facebook_api, extract_content as extract_facebook
    FACEBOOK_AVAILABLE = True
except:
    FACEBOOK_AVAILABLE = False

try:
    from odoo_integration_example import OdooClient
    ODOO_AVAILABLE = True
except:
    ODOO_AVAILABLE = False


class GoldTierAutonomous:
    """Full autonomous system - Gold Tier"""
    
    def __init__(self):
        self.folders = {
            'inbox': '00_Inbox',
            'drafts': '01_Drafts/Auto_Generated',
            'pending_social': '02_Pending_Approvals/Social_Posts',
            'pending_email': '02_Pending_Approvals/Email_Drafts',
            'posted': '03_Posted/History',
            'urgent': '00_Inbox/Urgent_WhatsApp',
            'alerts': '00_Inbox/ALERTS.md'
        }
        
        self.check_interval = 900  # 15 minutes
        self.last_post_generation = None
        self.post_generation_interval = 43200  # 12 hours
        
        self.status_file = 'System_Live_Status.md'
        
        # Ensure folders exist
        self.ensure_folders()
        
    def ensure_folders(self):
        """Create all required folders"""
        for folder in self.folders.values():
            if folder.endswith('.md'):
                continue
            Path(folder).mkdir(parents=True, exist_ok=True)
        print("✅ All folders verified")
    
    def update_system_status(self):
        """Update System_Live_Status.md"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        status = f"""# 🤖 Gold Tier System Live Status

**Last Updated**: {timestamp}

## 🌐 Platform Connectivity

| Platform | Status | Method | Last Check |
|----------|--------|--------|------------|
| LinkedIn | {'✅ Connected' if LINKEDIN_AVAILABLE else '❌ Offline'} | Playwright | {timestamp} |
| Twitter/X | {'✅ Connected' if TWITTER_AVAILABLE else '❌ Offline'} | OAuth 1.0a | {timestamp} |
| Facebook | {'✅ Connected' if FACEBOOK_AVAILABLE else '❌ Offline'} | Graph API | {timestamp} |
| Odoo | {'✅ Connected' if ODOO_AVAILABLE else '❌ Offline'} | JSON-RPC | {timestamp} |

## 📊 System Metrics

- **Check Interval**: {self.check_interval // 60} minutes
- **Post Generation**: Every {self.post_generation_interval // 3600} hours
- **Last Post Gen**: {self.last_post_generation or 'Never'}
- **Mode**: Ralph Wiggum Loop (Autonomous)

## 🔄 Active Processes

- ✅ Social Media Monitoring
- ✅ Auto-Post Generation
- ✅ File Watcher Active
- ✅ Error Logging Enabled

## 📁 Folder Status

- Inbox: `{self.folders['inbox']}`
- Drafts: `{self.folders['drafts']}`
- Pending: `{self.folders['pending_social']}`
- Posted: `{self.folders['posted']}`

## 🎯 Next Actions

- Next post generation: {self._next_post_time()}
- Next check: {self._next_check_time()}

---
*System running in autonomous mode. Press Ctrl+C to stop.*
"""
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            f.write(status)
    
    def _next_post_time(self):
        """Calculate next post generation time"""
        if not self.last_post_generation:
            return "Soon"
        next_time = datetime.fromisoformat(self.last_post_generation) + timedelta(seconds=self.post_generation_interval)
        return next_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def _next_check_time(self):
        """Calculate next check time"""
        next_time = datetime.now() + timedelta(seconds=self.check_interval)
        return next_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def log_error(self, message):
        """Log error"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('System_Errors.md', 'a', encoding='utf-8') as f:
            f.write(f"\n## Error - {timestamp}\n{message}\n\n")
        print(f"❌ {message}")
    
    def create_alert(self, message):
        """Create alert"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.folders['alerts'], 'a', encoding='utf-8') as f:
            f.write(f"\n## ALERT - {timestamp}\n{message}\n\n")
        print(f"🚨 {message}")
    
    def generate_posts(self):
        """Generate posts for all platforms"""
        try:
            from autonomous_social_agent import AutonomousSocialAgent
            agent = AutonomousSocialAgent()
            
            platforms = ['LinkedIn', 'Twitter', 'Facebook', 'Instagram']
            
            for platform in platforms:
                try:
                    content = agent.generate_social_post(platform)
                    filepath = agent.create_pending_post(platform, content)
                    print(f"✅ Generated {platform} post: {filepath}")
                except Exception as e:
                    self.log_error(f"Failed to generate {platform} post: {str(e)}")
            
            self.last_post_generation = datetime.now().isoformat()
            
        except Exception as e:
            self.log_error(f"Post generation error: {str(e)}")
    
    def should_generate_posts(self):
        """Check if it's time to generate new posts"""
        if not self.last_post_generation:
            return True
        
        last_time = datetime.fromisoformat(self.last_post_generation)
        time_diff = datetime.now() - last_time
        return time_diff.total_seconds() >= self.post_generation_interval
    
    def post_linkedin(self, filepath):
        """Post to LinkedIn"""
        if not LINKEDIN_AVAILABLE:
            return False
        try:
            return post_to_linkedin(str(filepath), headless=True)
        except Exception as e:
            self.log_error(f"LinkedIn error: {str(e)}")
            return False
    
    def post_twitter(self, filepath):
        """Post to Twitter"""
        if not TWITTER_AVAILABLE:
            return False
        try:
            content = extract_twitter(filepath)
            return post_tweet_oauth(content)
        except Exception as e:
            self.log_error(f"Twitter error: {str(e)}")
            return False
    
    def post_facebook(self, filepath):
        """Post to Facebook"""
        if not FACEBOOK_AVAILABLE:
            return False
        try:
            content = extract_facebook(filepath)
            result = post_to_facebook_api(content)
            if not result:
                # If posting fails, log specific error and suggest token refresh
                self.log_error(f"Facebook posting failed for {filepath.name}. Token may be expired.")
                self.create_alert(f"Facebook token expired. Run: python fix_facebook_instagram_tokens.py")
            return result
        except Exception as e:
            self.log_error(f"Facebook error: {str(e)}")
            return False
    def post_instagram(self, filepath):
        """Post to Instagram using text-to-image conversion"""
        try:
            import subprocess
            print("📸 Converting text to image for Instagram...")
            result = subprocess.run(['python', 'instagram_text_to_image.py', str(filepath)],
                                  capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                print("✅ Instagram post prepared (image generated)")
                return True
            else:
                print(f"❌ Instagram preparation failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_error(f"Instagram error: {str(e)}")
            return False
    
    def check_approved_posts(self):
        """Check for approved posts and auto-post"""
        posted_folder = Path(self.folders['posted'])
        
        for filepath in posted_folder.glob('*.md'):
            if filepath.name.startswith('POSTED_'):
                continue
            
            platform = filepath.name.split('_')[0]
            print(f"\n📤 Processing {platform} post: {filepath.name}")
            
            success = False
            
            if platform == 'LinkedIn' and LINKEDIN_AVAILABLE:
                success = self.post_linkedin(filepath)
            elif platform == 'Twitter' and TWITTER_AVAILABLE:
                success = self.post_twitter(filepath)
            elif platform == 'Facebook' and FACEBOOK_AVAILABLE:
                success = self.post_facebook(filepath)
            elif platform == 'Instagram':
                success = self.post_instagram(filepath)
            else:
                print(f"⚠️  {platform} posting not available")
                continue
            
            if success:
                new_name = f"POSTED_{filepath.name}"
                new_path = filepath.parent / new_name
                filepath.rename(new_path)
                print(f"✅ Posted and renamed to: {new_name}")
            else:
                error_msg = f"Failed to post {platform}: {filepath.name}"
                self.log_error(error_msg)
                self.create_alert(error_msg)
    
    def update_odoo_dashboard(self):
        """Update dashboard with Odoo data (Monday mornings)"""
        if not ODOO_AVAILABLE:
            return
        
        now = datetime.now()
        if now.weekday() != 0 or now.hour != 8:  # Monday at 8 AM
            return
        
        try:
            client = OdooClient()
            client.authenticate()
            summary = client.get_accounting_summary()
            
            # Update Dashboard.md
            dashboard_content = f"""
# CEO Briefing - {now.strftime('%Y-%m-%d')}

## Odoo Accounting Summary

- **Total Customers**: {summary['customers']['total']}
- **Total Invoices**: {summary['invoices']['total']}
- **Unpaid Invoices**: {summary['invoices']['unpaid_count']}
- **Unpaid Amount**: ${summary['invoices']['unpaid_amount']:.2f}

---
*Auto-generated by Gold Tier System*
"""
            
            with open('Dashboard.md', 'a', encoding='utf-8') as f:
                f.write(dashboard_content)
            
            print("✅ Dashboard updated with Odoo data")
            
        except Exception as e:
            self.log_error(f"Odoo dashboard update error: {str(e)}")
    
    def run(self):
        """Main Ralph Wiggum Loop"""
        print("=" * 60)
        print("🏆 GOLD TIER AUTONOMOUS SYSTEM")
        print("=" * 60)
        print()
        print("🤖 Ralph Wiggum Loop Mode: ACTIVE")
        print()
        print("Available platforms:")
        print(f"  - LinkedIn: {'✅' if LINKEDIN_AVAILABLE else '❌'}")
        print(f"  - Twitter: {'✅' if TWITTER_AVAILABLE else '❌'}")
        print(f"  - Facebook: {'✅' if FACEBOOK_AVAILABLE else '❌'}")
        print(f"  - Odoo: {'✅' if ODOO_AVAILABLE else '❌'}")
        print()
        print(f"⏰ Check Interval: {self.check_interval // 60} minutes")
        print(f"📝 Post Generation: Every {self.post_generation_interval // 3600} hours")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
        
        iteration = 0
        
        while True:
            try:
                iteration += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n🔄 Iteration #{iteration} - {timestamp}")
                print("-" * 60)
                
                # 1. Update system status
                self.update_system_status()
                print("✅ System status updated")
                
                # 2. Generate posts if needed
                if self.should_generate_posts():
                    print("📝 Generating new posts...")
                    self.generate_posts()
                
                # 3. Check and post approved content
                self.check_approved_posts()
                
                # 4. Update Odoo dashboard (Monday mornings)
                self.update_odoo_dashboard()
                
                print(f"✅ Iteration #{iteration} complete")
                print(f"⏳ Next check in {self.check_interval // 60} minutes...")
                print(f"📊 Status: {self.status_file}")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping Gold Tier System...")
                print("✅ Shutdown complete")
                break
                
            except Exception as e:
                self.log_error(f"Loop error: {str(e)}")
                print(f"❌ {str(e)}")
                print("🔄 Continuing...")
                time.sleep(60)


def main():
    """Start Gold Tier Autonomous System"""
    system = GoldTierAutonomous()
    system.run()


if __name__ == "__main__":
    main()
