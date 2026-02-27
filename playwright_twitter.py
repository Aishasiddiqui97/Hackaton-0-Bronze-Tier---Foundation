#!/usr/bin/env python3
"""
Twitter/X Poster using Playwright
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

load_dotenv()

TWITTER_EMAIL = os.getenv('TWITTER_EMAIL', '')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', '')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD', '')


class TwitterPosterPlaywright:
    """Twitter/X automation using Playwright"""
    
    def __init__(self, headless=True):
        self.email = TWITTER_EMAIL
        self.username = TWITTER_USERNAME
        self.password = TWITTER_PASSWORD
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        
    def start(self):
        """Start browser"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        self.page = context.new_page()
        print("✅ Browser started")
        
    def login(self):
        """Login to Twitter/X"""
        try:
            print("🔐 Logging into Twitter/X...")
            self.page.goto('https://twitter.com/i/flow/login', wait_until='networkidle')
            time.sleep(3)
            
            # Enter username/email
            self.page.fill('input[autocomplete="username"]', self.username or self.email)
            self.page.click('button:has-text("Next")')
            time.sleep(2)
            
            # Sometimes Twitter asks for email verification
            try:
                if self.page.is_visible('input[data-testid="ocfEnterTextTextInput"]'):
                    self.page.fill('input[data-testid="ocfEnterTextTextInput"]', self.email)
                    self.page.click('button:has-text("Next")')
                    time.sleep(2)
            except:
                pass
            
            # Enter password
            self.page.fill('input[name="password"]', self.password)
            self.page.click('button[data-testid="LoginForm_Login_Button"]')
            
            time.sleep(5)
            
            if 'home' in self.page.url:
                print("✅ Login successful!")
                return True
            else:
                print("⚠️  Login may have failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def post_tweet(self, content):
        """Post tweet"""
        try:
            print("📝 Creating tweet...")
            
            # Go to home
            self.page.goto('https://twitter.com/home', wait_until='networkidle')
            time.sleep(3)
            
            # Click tweet button or find compose box
            try:
                # Try clicking "What's happening" box
                self.page.click('div[data-testid="tweetTextarea_0"]')
                time.sleep(1)
            except:
                # Try clicking tweet button
                self.page.click('a[data-testid="SideNav_NewTweet_Button"]')
                time.sleep(2)
            
            # Type content
            self.page.fill('div[data-testid="tweetTextarea_0"]', content)
            time.sleep(2)
            
            # Click Tweet button
            self.page.click('button[data-testid="tweetButtonInline"]')
            time.sleep(3)
            
            print("✅ Successfully posted tweet!")
            return True
            
        except Exception as e:
            print(f"❌ Error posting: {e}")
            self.page.screenshot(path='error_twitter.png')
            return False
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("🔒 Browser closed")


def extract_content(filepath):
    """Extract content from markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    post_lines = []
    in_content = False
    
    for line in lines:
        if '## Content' in line:
            in_content = True
            continue
        elif line.startswith('##') and in_content:
            break
        elif in_content and line.strip() and not line.strip().startswith('#'):
            post_lines.append(line.strip())
    
    # Twitter has 280 char limit
    full_content = '\n\n'.join(post_lines)
    if len(full_content) > 280:
        full_content = full_content[:277] + '...'
    
    return full_content


def post_to_twitter(filepath, headless=True):
    """Main function to post to Twitter"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed")
        return False
    
    if not TWITTER_EMAIL or not TWITTER_PASSWORD:
        print("❌ Twitter credentials not found in .env")
        return False
    
    poster = None
    
    try:
        print("=" * 60)
        print("Twitter/X Poster (Playwright)")
        print("=" * 60)
        print()
        
        # Extract content
        content = extract_content(filepath)
        print(f"📄 Content: {len(content)} characters")
        print()
        
        # Initialize poster
        poster = TwitterPosterPlaywright(headless=headless)
        poster.start()
        
        # Login
        if not poster.login():
            return False
        
        # Post
        success = poster.post_tweet(content)
        
        if success:
            print()
            print("=" * 60)
            print("✅ SUCCESS! Posted to Twitter/X")
            print("=" * 60)
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if poster:
            time.sleep(2)
            poster.close()


def main():
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*Twitter_Post_*.md'))
        
        if not posts:
            print("❌ No Twitter posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    post_to_twitter(str(filepath), headless=False)


if __name__ == "__main__":
    main()
