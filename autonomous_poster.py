#!/usr/bin/env python3
"""
Autonomous Social Media Poster - Ralph Wiggum Loop
Watches for approved posts and automatically posts them
"""

import os
import time
from datetime import datetime
from pathlib import Path
import shutil

# Import platform posters
try:
    from playwright_linkedin import post_to_linkedin
    from playwright_twitter import post_to_twitter
    from playwright_facebook import post_to_facebook
    PLAYWRIGHT_AVAILABLE = True
except:
    PLAYWRIGHT_AVAILABLE = False


class AutonomousPoster:
    """Autonomous posting system"""
    
    def __init__(self):
        self.folders = {
            'pending': '02_Pending_Approvals/Social_Posts',
            'posted': '03_Posted/History',
            'inbox': '00_Inbox',
            'alerts': '00_Inbox/ALERTS.md',
            'errors': 'System_Errors.md'
        }
        
        self.platform_handlers = {
            'LinkedIn': post_to_linkedin,
            'Twitter': post_to_twitter,
            'Facebook': post_to_facebook
        }
        
        self.check_interval = 900  # 15 minutes in seconds
        
    def log_error(self, message):
        """Log error to System_Errors.md"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"\n## Error - {timestamp}\n{message}\n\n"
        
        with open(self.folders['errors'], 'a', encoding='utf-8') as f:
            f.write(error_msg)
        
        print(f"❌ Error logged: {message}")
    
    def create_alert(self, message):
        """Create alert in inbox"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_msg = f"\n## ALERT - {timestamp}\n{message}\n\n"
        
        with open(self.folders['alerts'], 'a', encoding='utf-8') as f:
            f.write(alert_msg)
        
        print(f"🚨 Alert created: {message}")
    
    def check_approved_posts(self):
        """Check for approved posts in Posted folder"""
        posted_folder = Path(self.folders['posted'])
        
        for filepath in posted_folder.glob('*.md'):
            # Skip already posted files
            if filepath.name.startswith('POSTED_'):
                continue
            
            # Extract platform from filename
            platform = filepath.name.split('_')[0]
            
            if platform not in self.platform_handlers:
                print(f"⚠️  Unknown platform: {platform}")
                continue
            
            print(f"\n📤 Processing {platform} post: {filepath.name}")
            
            # Post to platform
            try:
                handler = self.platform_handlers[platform]
                success = handler(str(filepath), headless=True)
                
                if success:
                    # Mark as posted
                    new_name = f"POSTED_{filepath.name}"
                    new_path = filepath.parent / new_name
                    filepath.rename(new_path)
                    
                    print(f"✅ Successfully posted to {platform}")
                    print(f"✅ Renamed to: {new_name}")
                    
                else:
                    error_msg = f"Failed to post to {platform}: {filepath.name}"
                    self.log_error(error_msg)
                    self.create_alert(error_msg)
                    
            except Exception as e:
                error_msg = f"Exception posting to {platform}: {str(e)}"
                self.log_error(error_msg)
                self.create_alert(error_msg)
    
    def ralph_wiggum_loop(self):
        """Main autonomous loop"""
        print("=" * 60)
        print("🤖 Autonomous Social Media Poster")
        print("=" * 60)
        print()
        print("📋 Ralph Wiggum Loop Active")
        print(f"⏰ Check Interval: {self.check_interval // 60} minutes")
        print()
        print("Monitoring:")
        print(f"  - {self.folders['posted']}")
        print()
        print("Will auto-post to:")
        print("  - LinkedIn")
        print("  - Twitter/X")
        print("  - Facebook")
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
                
                # Check for approved posts
                self.check_approved_posts()
                
                print(f"✅ Iteration #{iteration} complete")
                print(f"⏳ Next check in {self.check_interval // 60} minutes...")
                
                # Wait for next iteration
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping autonomous poster...")
                print("✅ Shutdown complete")
                break
                
            except Exception as e:
                error_msg = f"Error in main loop: {str(e)}"
                self.log_error(error_msg)
                print(f"❌ {error_msg}")
                print("🔄 Continuing...")
                time.sleep(60)  # Wait 1 minute before retry


def main():
    """Start autonomous poster"""
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available")
        print("💡 Run: setup_playwright.bat")
        return
    
    poster = AutonomousPoster()
    poster.ralph_wiggum_loop()


if __name__ == "__main__":
    main()
