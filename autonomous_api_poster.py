#!/usr/bin/env python3
"""
Autonomous API-Based Social Media Poster
Uses official APIs instead of browser automation (more reliable)
"""

import os
import time
from datetime import datetime
from pathlib import Path

# Import API posters
try:
    from playwright_linkedin import post_to_linkedin
    LINKEDIN_AVAILABLE = True
except:
    LINKEDIN_AVAILABLE = False

try:
    from api_twitter_poster import post_tweet_api, extract_content as extract_twitter
    TWITTER_AVAILABLE = True
except:
    TWITTER_AVAILABLE = False

try:
    from api_facebook_poster import post_to_facebook_api, extract_content as extract_facebook
    FACEBOOK_AVAILABLE = True
except:
    FACEBOOK_AVAILABLE = False


class AutonomousAPIPoster:
    """Autonomous posting using APIs"""
    
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
    
    def create_alert(self, message):
        """Create alert"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.folders['alerts'], 'a', encoding='utf-8') as f:
            f.write(f"\n## ALERT - {timestamp}\n{message}\n\n")
        print(f"🚨 {message}")
    
    def post_linkedin(self, filepath):
        """Post to LinkedIn using Playwright"""
        if not LINKEDIN_AVAILABLE:
            return False
        try:
            return post_to_linkedin(str(filepath), headless=True)
        except Exception as e:
            self.log_error(f"LinkedIn error: {str(e)}")
            return False
    
    def post_twitter(self, filepath):
        """Post to Twitter using API"""
        if not TWITTER_AVAILABLE:
            return False
        try:
            content = extract_twitter(filepath)
            return post_tweet_api(content)
        except Exception as e:
            self.log_error(f"Twitter error: {str(e)}")
            return False
    
    def post_facebook(self, filepath):
        """Post to Facebook using API"""
        if not FACEBOOK_AVAILABLE:
            return False
        try:
            content = extract_facebook(filepath)
            return post_to_facebook_api(content)
        except Exception as e:
            self.log_error(f"Facebook error: {str(e)}")
            return False
    
    def check_approved_posts(self):
        """Check for approved posts"""
        posted_folder = Path(self.folders['posted'])
        
        for filepath in posted_folder.glob('*.md'):
            # Skip already posted
            if filepath.name.startswith('POSTED_'):
                continue
            
            # Extract platform
            platform = filepath.name.split('_')[0]
            
            print(f"\n📤 Processing {platform} post: {filepath.name}")
            
            # Post based on platform
            success = False
            
            if platform == 'LinkedIn' and LINKEDIN_AVAILABLE:
                success = self.post_linkedin(filepath)
            elif platform == 'Twitter' and TWITTER_AVAILABLE:
                success = self.post_twitter(filepath)
            elif platform == 'Facebook' and FACEBOOK_AVAILABLE:
                success = self.post_facebook(filepath)
            else:
                print(f"⚠️  {platform} posting not available")
                continue
            
            if success:
                # Rename as posted
                new_name = f"POSTED_{filepath.name}"
                new_path = filepath.parent / new_name
                filepath.rename(new_path)
                print(f"✅ Posted and renamed to: {new_name}")
            else:
                error_msg = f"Failed to post {platform}: {filepath.name}"
                self.log_error(error_msg)
                self.create_alert(error_msg)
    
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("🤖 Autonomous API-Based Poster")
        print("=" * 60)
        print()
        print("Available platforms:")
        print(f"  - LinkedIn: {'✅' if LINKEDIN_AVAILABLE else '❌'}")
        print(f"  - Twitter: {'✅' if TWITTER_AVAILABLE else '❌'}")
        print(f"  - Facebook: {'✅' if FACEBOOK_AVAILABLE else '❌'}")
        print()
        print(f"📋 Monitoring: {self.folders['posted']}")
        print(f"⏰ Check Interval: {self.check_interval // 60} minutes")
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
                
                self.check_approved_posts()
                
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
    poster = AutonomousAPIPoster()
    poster.run()


if __name__ == "__main__":
    main()
