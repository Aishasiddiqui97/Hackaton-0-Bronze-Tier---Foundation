#!/usr/bin/env python3
"""
LinkedIn Poster using Playwright (More Reliable than Selenium)
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Run: setup_playwright.bat")

load_dotenv()

LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


class LinkedInPosterPlaywright:
    """LinkedIn automation using Playwright"""
    
    def __init__(self, headless=True):
        self.email = LINKEDIN_EMAIL
        self.password = LINKEDIN_PASSWORD
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        
    def start(self):
        """Start browser"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        self.page = context.new_page()
        print("✅ Browser started")
        
    def login(self):
        """Login to LinkedIn"""
        try:
            print("🔐 Logging into LinkedIn...")
            self.page.goto('https://www.linkedin.com/login', wait_until='networkidle')
            
            # Enter email
            self.page.fill('#username', self.email)
            
            # Enter password
            self.page.fill('#password', self.password)
            
            # Click login
            self.page.click('button[type="submit"]')
            
            # Wait for navigation
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Check if logged in
            if 'feed' in self.page.url or 'mynetwork' in self.page.url:
                print("✅ Login successful!")
                return True
            else:
                print("⚠️  Login may have failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def post_content(self, content):
        """Post content to LinkedIn"""
        try:
            print("📝 Creating LinkedIn post...")
            
            # Go to feed
            self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            time.sleep(3)
            
            # Click "Start a post" - try multiple selectors
            selectors = [
                'button:has-text("Start a post")',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]'
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    clicked = True
                    print(f"✅ Clicked start post button")
                    break
                except:
                    continue
            
            if not clicked:
                print("❌ Could not find start post button")
                self.page.screenshot(path='error_start_post.png')
                return False
            
            time.sleep(2)
            
            # Find editor and type content
            editor_selectors = [
                'div.ql-editor[contenteditable="true"]',
                'div[role="textbox"]',
                'div.ql-editor'
            ]
            
            typed = False
            for selector in editor_selectors:
                try:
                    self.page.fill(selector, content)
                    typed = True
                    print("✅ Content entered")
                    break
                except:
                    continue
            
            if not typed:
                print("❌ Could not enter content")
                self.page.screenshot(path='error_content.png')
                return False
            
            time.sleep(2)
            
            # Click Post button
            post_selectors = [
                'button:has-text("Post")',
                'button.share-actions__primary-action',
                '[data-control-name="share.post"]'
            ]
            
            posted = False
            for selector in post_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    posted = True
                    print("✅ Post button clicked")
                    break
                except:
                    continue
            
            if not posted:
                print("❌ Could not click Post button")
                self.page.screenshot(path='error_post_button.png')
                return False
            
            time.sleep(5)
            
            print("✅ Successfully posted to LinkedIn!")
            return True
            
        except Exception as e:
            print(f"❌ Error posting: {e}")
            self.page.screenshot(path='error_general.png')
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


def post_to_linkedin(filepath, headless=True):
    """Main function to post to LinkedIn"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed")
        return False
    
    poster = None
    
    try:
        print("=" * 60)
        print("LinkedIn Poster (Playwright)")
        print("=" * 60)
        print()
        
        # Extract content
        content = extract_content(filepath)
        print(f"📄 Content: {len(content)} characters")
        print()
        
        # Initialize poster
        poster = LinkedInPosterPlaywright(headless=headless)
        poster.start()
        
        # Login
        if not poster.login():
            return False
        
        # Post
        success = poster.post_content(content)
        
        if success:
            print()
            print("=" * 60)
            print("✅ SUCCESS! Posted to LinkedIn")
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
        # Find latest approved post
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        
        if not posts:
            print("❌ No LinkedIn posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    # Post
    success = post_to_linkedin(str(filepath), headless=False)
    
    if not success:
        print("\n❌ Posting failed")
        print("💡 Check error screenshots")


if __name__ == "__main__":
    main()
