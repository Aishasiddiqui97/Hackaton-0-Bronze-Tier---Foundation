#!/usr/bin/env python3
"""
Autonomous LinkedIn-Only Poster
For when only LinkedIn credentials are available
"""

import os
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright_linkedin import post_to_linkedin
    PLAYWRIGHT_AVAILABLE = True
except:
    PLAYWRIGHT_AVAILABLE = False


class LinkedInOnlyPoster:
    """Autonomous posting for LinkedIn only"""
    
    def __init__(self):
        self.folders = {
            'posted': '03_Posted/History',
            'errors': 'System_Errors.md',
            'alerts': '00_Inbox/ALERTS.md'
        }
        self.check_interval = 900  # 15 minutes
        
    def log_error(self, message):
        """Log error"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.folders['errors'], 'a', encoding='utf-8') as f:
            f.write(f"\n## Error - {timestamp}\n{message}\n\n")
        print(f"❌ {message}")
    
    def check_linkedin_posts(self):
        """Check for LinkedIn posts only"""
        posted_folder = Path(self.folders['posted'])
        
        for filepath in posted_folder.glob('LinkedIn_Post_*.md'):
            # Skip already posted
            if filepath.name.startswith('POSTED_'):
                continue
            
            print(f"\n📤 Processing LinkedIn post: {filepath.name}")
            
            try:
                success = post_to_linkedin(str(filepath), headless=True)
                
                if success:
                    # Rename
                    new_name = f"POSTED_{filepath.name}"
                    new_path = filepath.parent / new_name
                    filepath.rename(new_path)
                    print(f"✅ Posted and renamed to: {new_name}")
                else:
                    self.log_error(f"Failed to post: {filepath.name}")
                    
            except Exception as e:
                self.log_error(f"Exception: {str(e)}")
    
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("🔵 Autonomous LinkedIn Poster")
        print("=" * 60)
        print()
        print("📋 Monitoring: 03_Posted/History/")
        print(f"⏰ Check Interval: {self.check_interval // 60} minutes")
        print()
        print("Will auto-post LinkedIn posts only")
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
                
                self.check_linkedin_posts()
                
                print(f"✅ Iteration #{iteration} complete")
                print(f"⏳ Next check in {self.check_interval // 60} minutes...")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping...")
                break
            except Exception as e:
                self.log_error(f"Loop error: {str(e)}")
                time.sleep(60)


def main():
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available")
        print("💡 Run: setup_playwright.bat")
        return
    
    poster = LinkedInOnlyPoster()
    poster.run()


if __name__ == "__main__":
    main()
