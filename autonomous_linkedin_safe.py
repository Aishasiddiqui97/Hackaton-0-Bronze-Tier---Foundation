#!/usr/bin/env python3
"""
Autonomous LinkedIn Poster - Unicode Safe Version
Uses the fixed Selenium implementation with emoji support
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8')

try:
    from linkedin_selenium_fixed import post_to_linkedin_safe
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False
    print("❌ LinkedIn safe poster not available")


class LinkedInSafePoster:
    """Autonomous LinkedIn posting with Unicode safety"""
    
    def __init__(self):
        self.folders = {
            'posted': '03_Posted/History',
            'errors': 'System_Errors.md',
            'alerts': '00_Inbox/ALERTS.md'
        }
        self.check_interval = 900  # 15 minutes
        
    def log_error(self, message):
        """Log error with Unicode safety"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.folders['errors'], 'a', encoding='utf-8') as f:
                f.write(f"\n## Error - {timestamp}\n{message}\n\n")
        except Exception as e:
            print(f"⚠️  Logging error: {e}")
        print(f"❌ {message}")
    
    def create_alert(self, message):
        """Create alert with Unicode safety"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.folders['alerts'], 'a', encoding='utf-8') as f:
                f.write(f"\n## ALERT - {timestamp}\n{message}\n\n")
        except Exception as e:
            print(f"⚠️  Alert creation error: {e}")
        print(f"🚨 {message}")
    
    def check_linkedin_posts(self):
        """Check for LinkedIn posts and post them safely"""
        posted_folder = Path(self.folders['posted'])
        
        if not posted_folder.exists():
            print("⚠️  Posted folder not found")
            return
        
        # Find unposted LinkedIn files
        linkedin_posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        unposted = [p for p in linkedin_posts if not p.name.startswith('POSTED_')]
        
        if not unposted:
            print("✅ No pending LinkedIn posts")
            return
        
        print(f"📋 Found {len(unposted)} pending LinkedIn posts")
        
        for filepath in unposted:
            print(f"\n📤 Processing: {filepath.name}")
            
            try:
                # Use the safe Unicode posting method
                success = post_to_linkedin_safe(str(filepath), headless=True)
                
                if success:
                    # Rename to mark as posted
                    new_name = f"POSTED_{filepath.name}"
                    new_path = filepath.parent / new_name
                    filepath.rename(new_path)
                    print(f"✅ Posted and renamed to: {new_name}")
                    
                    # Log success
                    self.log_success(f"Successfully posted: {filepath.name}")
                    
                else:
                    error_msg = f"Failed to post: {filepath.name}"
                    self.log_error(error_msg)
                    self.create_alert(error_msg)
                    
            except Exception as e:
                error_msg = f"Exception posting {filepath.name}: {str(e)}"
                self.log_error(error_msg)
                self.create_alert(error_msg)
            
            # Wait between posts to avoid rate limiting
            time.sleep(10)
    
    def log_success(self, message):
        """Log successful operations"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open('System_Success.md', 'a', encoding='utf-8') as f:
                f.write(f"\n## Success - {timestamp}\n{message}\n\n")
        except Exception as e:
            print(f"⚠️  Success logging error: {e}")
        print(f"✅ {message}")
    
    def update_status(self):
        """Update system status"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Count posts
        posted_folder = Path(self.folders['posted'])
        if posted_folder.exists():
            all_posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
            posted_count = len([p for p in all_posts if p.name.startswith('POSTED_')])
            pending_count = len(all_posts) - posted_count
        else:
            posted_count = pending_count = 0
        
        status = f"""# 🔵 LinkedIn Safe Poster Status

**Last Updated**: {timestamp}

## 📊 Statistics

- **Posted**: {posted_count}
- **Pending**: {pending_count}
- **Total**: {posted_count + pending_count}

## 🛡️ Safety Features

- ✅ Unicode/Emoji Support
- ✅ ChromeDriver BMP Compatibility  
- ✅ Windows Terminal Encoding Fix
- ✅ JavaScript Injection Method
- ✅ Multiple Selector Strategies
- ✅ Robust Error Handling

## 🔄 System Status

- **Mode**: Autonomous
- **Check Interval**: {self.check_interval // 60} minutes
- **LinkedIn Module**: {'✅ Available' if LINKEDIN_AVAILABLE else '❌ Not Available'}

---
*Safe autonomous LinkedIn posting with full Unicode support*
"""
        
        try:
            with open('LinkedIn_Status.md', 'w', encoding='utf-8') as f:
                f.write(status)
        except Exception as e:
            print(f"⚠️  Status update error: {e}")
    
    def run(self):
        """Main autonomous loop"""
        print("=" * 70)
        print("🔵 LinkedIn Safe Autonomous Poster")
        print("=" * 70)
        print()
        print("🛡️  Features:")
        print("   - Unicode/Emoji Support ✅")
        print("   - ChromeDriver BMP Fix ✅")
        print("   - Windows Encoding Fix ✅")
        print("   - JavaScript Injection ✅")
        print("   - Multiple Selectors ✅")
        print()
        print(f"📋 Monitoring: {self.folders['posted']}")
        print(f"⏰ Check Interval: {self.check_interval // 60} minutes")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 70)
        print()
        
        if not LINKEDIN_AVAILABLE:
            print("❌ LinkedIn safe module not available")
            print("💡 Make sure linkedin_selenium_fixed.py exists")
            return
        
        iteration = 0
        
        while True:
            try:
                iteration += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n🔄 Iteration #{iteration} - {timestamp}")
                print("-" * 70)
                
                # Update status
                self.update_status()
                
                # Check and post LinkedIn content
                self.check_linkedin_posts()
                
                print(f"✅ Iteration #{iteration} complete")
                print(f"⏳ Next check in {self.check_interval // 60} minutes...")
                print(f"📊 Status: LinkedIn_Status.md")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping LinkedIn Safe Poster...")
                print("✅ Shutdown complete")
                break
                
            except Exception as e:
                error_msg = f"Loop error: {str(e)}"
                self.log_error(error_msg)
                print(f"❌ {error_msg}")
                print("🔄 Continuing in 60 seconds...")
                time.sleep(60)


def main():
    """Start LinkedIn Safe Autonomous Poster"""
    poster = LinkedInSafePoster()
    poster.run()


if __name__ == "__main__":
    main()