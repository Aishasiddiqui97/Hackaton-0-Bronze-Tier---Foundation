#!/usr/bin/env python3
"""
Facebook Poster using Playwright
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

FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL', '')
FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD', '')


class FacebookPosterPlaywright:
    """Facebook automation using Playwright"""
    
    def __init__(self, headless=True):
        self.email = FACEBOOK_EMAIL
        self.password = FACEBOOK_PASSWORD
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
        """Login to Facebook"""
        try:
            print("🔐 Logging into Facebook...")
            self.page.goto('https://www.facebook.com/login', wait_until='networkidle')
            time.sleep(2)
            
            # Enter email
            self.page.fill('input[name="email"]', self.email)
            
            # Enter password
            self.page.fill('input[name="pass"]', self.password)
            
            # Click login
            self.page.click('button[name="login"]')
            
            time.sleep(5)
            
            if 'facebook.com' in self.page.url and 'login' not in self.page.url:
                print("✅ Login successful!")
                return True
            else:
                print("⚠️  Login may have failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def post_content(self, content):
        """Post to Facebook"""
        try:
            print("📝 Creating Facebook post...")
            
            # Go to home
            self.page.goto('https://www.facebook.com/', wait_until='networkidle')
            time.sleep(3)
            
            # Click "What's on your mind" box
            selectors = [
                'div[aria-label*="What\'s on your mind"]',
                'div[role="button"][tabindex="0"]',
                'span:has-text("What\'s on your mind")'
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                print("❌ Could not find post box")
                self.page.screenshot(path='error_fb_post_box.png')
                return False
            
            time.sleep(2)
            
            # Type content
            self.page.fill('div[contenteditable="true"]', content)
            time.sleep(2)
            
            # Click Post button
            post_selectors = [
                'div[aria-label="Post"]',
                'div[role="button"]:has-text("Post")'
            ]
            
            posted = False
            for selector in post_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    posted = True
                    break
                except:
                    continue
            
            if not posted:
                print("❌ Could not click Post button")
                self.page.screenshot(path='error_fb_post_button.png')
                return False
            
            time.sleep(5)
            
            print("✅ Successfully posted to Facebook!")
            return True
            
        except Exception as e:
            print(f"❌ Error posting: {e}")
            self.page.screenshot(path='error_facebook.png')
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
    
    return '\n\n'.join(post_lines)


def post_to_facebook(filepath, headless=True):
    """Main function to post to Facebook"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed")
        return False
    
    if not FACEBOOK_EMAIL or not FACEBOOK_PASSWORD:
        print("❌ Facebook credentials not found in .env")
        return False
    
    poster = None
    
    try:
        print("=" * 60)
        print("Facebook Poster (Playwright)")
        print("=" * 60)
        print()
        
        # Extract content
        content = extract_content(filepath)
        print(f"📄 Content: {len(content)} characters")
        print()
        
        # Initialize poster
        poster = FacebookPosterPlaywright(headless=headless)
        poster.start()
        
        # Login
        if not poster.login():
            return False
        
        # Post
        success = poster.post_content(content)
        
        if success:
            print()
            print("=" * 60)
            print("✅ SUCCESS! Posted to Facebook")
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
        posts = list(posted_folder.glob('*Facebook_Post_*.md'))
        
        if not posts:
            print("❌ No Facebook posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    post_to_facebook(str(filepath), headless=False)


if __name__ == "__main__":
    main()
