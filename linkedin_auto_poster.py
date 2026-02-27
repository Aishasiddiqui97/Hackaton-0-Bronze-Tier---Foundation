#!/usr/bin/env python3
"""
LinkedIn Auto-Poster using Selenium (Browser Automation)
No API required - uses email/password login
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import time
import random
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not installed. Run: pip install selenium")

load_dotenv()

LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


def clean_text_for_selenium(text):
    """Remove non-BMP characters (emoji safe for ChromeDriver)"""
    return re.sub(r'[^\u0000-\uFFFF]', '', text)


class LinkedInPoster:
    """Automate LinkedIn posting using Selenium"""
    
    def __init__(self, headless=False):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not installed. Run: pip install selenium")
        
        self.email = LINKEDIN_EMAIL
        self.password = LINKEDIN_PASSWORD
        self.driver = None
        self.headless = headless
        
        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials not found in .env file")
    
    def setup_driver(self):
        """Setup Chrome driver with anti-detection options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome driver initialized (stealth mode)")
        except Exception as e:
            print(f"❌ Error initializing Chrome driver: {e}")
            raise
    
    def login(self):
        """Login to LinkedIn with human-like behavior"""
        try:
            print("🔐 Logging into LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(3 + random.uniform(0.5, 1.5))
            
            email_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            time.sleep(random.uniform(0.3, 0.7))
            
            for char in self.email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            print(f"✅ Email entered")
            time.sleep(random.uniform(0.5, 1.0))
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            time.sleep(random.uniform(0.3, 0.7))
            
            for char in self.password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            print("✅ Password entered")
            time.sleep(random.uniform(0.5, 1.0))
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            time.sleep(random.uniform(0.3, 0.7))
            login_button.click()
            print("🔄 Login button clicked, waiting...")
            
            time.sleep(8 + random.uniform(1, 3))
            
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")
            
            if "feed" in current_url or "mynetwork" in current_url or "linkedin.com/in/" in current_url:
                print("✅ Login successful!")
                time.sleep(random.uniform(1, 2))
                return True
            elif "checkpoint" in current_url or "challenge" in current_url:
                print("⚠️  LinkedIn security checkpoint detected!")
                print("💡 Please complete the verification manually in the browser")
                print("⏳ Waiting 30 seconds for manual verification...")
                time.sleep(30)
                
                current_url = self.driver.current_url
                if "feed" in current_url or "mynetwork" in current_url:
                    print("✅ Verification complete! Login successful!")
                    return True
                else:
                    print("❌ Verification failed or incomplete")
                    return False
            else:
                print("⚠️  Login may have failed. Check credentials.")
                self.driver.save_screenshot('login_failed.png')
                print("📸 Screenshot saved: login_failed.png")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            try:
                self.driver.save_screenshot('login_error.png')
                print("📸 Screenshot saved: login_error.png")
            except:
                pass
            return False
    
    def create_post(self, content):
        """Create a LinkedIn post with Unicode/emoji safety"""
        try:
            print("📝 Creating LinkedIn post...")
            
            cleaned_content = clean_text_for_selenium(content)
            
            self.driver.get('https://www.linkedin.com/feed/')
            time.sleep(4 + random.uniform(1, 2))
            
            self.driver.execute_script("window.scrollTo(0, 300)")
            time.sleep(random.uniform(0.5, 1.0))
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(random.uniform(0.5, 1.0))
            
            start_post_selectors = [
                "button[aria-label*='Start a post']",
                "button.share-box-feed-entry__trigger",
                "button.artdeco-button--muted",
                "div.share-box-feed-entry__trigger",
                "//button[contains(text(), 'Start a post')]",
                "//div[contains(@class, 'share-box')]//button"
            ]
            
            start_post_button = None
            for selector in start_post_selectors:
                try:
                    if selector.startswith('//'):
                        start_post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        start_post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"✅ Found start post button")
                    break
                except:
                    continue
            
            if not start_post_button:
                print("❌ Could not find 'Start a post' button")
                self.driver.save_screenshot('error_start_post.png')
                return False
            
            time.sleep(random.uniform(0.3, 0.7))
            start_post_button.click()
            time.sleep(2 + random.uniform(0.5, 1.5))
            
            editor_selectors = [
                "div.ql-editor[contenteditable='true']",
                "div[role='textbox']",
                "div.ql-editor",
                "//div[@contenteditable='true']",
                "//div[@role='textbox']"
            ]
            
            text_editor = None
            for selector in editor_selectors:
                try:
                    if selector.startswith('//'):
                        text_editor = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        text_editor = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    print(f"✅ Found text editor")
                    break
                except:
                    continue
            
            if not text_editor:
                print("❌ Could not find text editor")
                self.driver.save_screenshot('error_text_editor.png')
                return False
            
            text_editor.click()
            time.sleep(random.uniform(0.5, 1.0))
            
            self.driver.execute_script(
                "arguments[0].focus(); arguments[0].innerText = arguments[1];",
                text_editor,
                cleaned_content
            )
            
            time.sleep(random.uniform(1, 2))
            
            post_button_selectors = [
                "button.share-actions__primary-action",
                "button[aria-label*='Post']",
                "//button[contains(text(), 'Post')]",
                "//button[@type='submit']",
                "button.artdeco-button--primary"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    if selector.startswith('//'):
                        post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"✅ Found post button")
                    break
                except:
                    continue
            
            if not post_button:
                print("❌ Could not find Post button")
                self.driver.save_screenshot('error_post_button.png')
                return False
            
            time.sleep(random.uniform(0.5, 1.0))
            post_button.click()
            
            print("✅ Post created successfully!")
            time.sleep(4 + random.uniform(1, 2))
            return True
            
        except Exception as e:
            print(f"❌ Error creating post: {e}")
            try:
                self.driver.save_screenshot('error_general.png')
                print("📸 Screenshot saved: error_general.png")
            except:
                pass
            return False
    
    def post_from_file(self, filepath):
        """Read post content from file and post to LinkedIn"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            post_content = []
            in_content_section = False
            
            for line in lines:
                if line.strip() == '## Content':
                    in_content_section = True
                    continue
                elif line.strip().startswith('##') and in_content_section:
                    break
                elif in_content_section and line.strip():
                    post_content.append(line.strip())
            
            final_content = '\n\n'.join(post_content)
            
            if not final_content:
                print("⚠️  No content found in file")
                return False
            
            print(f"📄 Content length: {len(final_content)} characters")
            
            return self.create_post(final_content)
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")


def post_to_linkedin(filepath):
    """Main function to post to LinkedIn"""
    poster = None
    
    try:
        print("=" * 60)
        print("LinkedIn Auto-Poster")
        print("=" * 60)
        print()
        
        poster = LinkedInPoster(headless=False)
        poster.setup_driver()
        
        if not poster.login():
            print("❌ Login failed. Check credentials in .env file")
            return False
        
        if poster.post_from_file(filepath):
            print()
            print("=" * 60)
            print("✅ Successfully posted to LinkedIn!")
            print("=" * 60)
            return True
        else:
            print("❌ Failed to post")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if poster:
            time.sleep(3)
            poster.close()


def main():
    """Test the LinkedIn poster"""
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        
        if not posts:
            print("❌ No LinkedIn posts found in 03_Posted/History/")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using latest post: {filepath.name}")
    
    post_to_linkedin(str(filepath))


if __name__ == "__main__":
    main()
