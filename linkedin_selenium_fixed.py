#!/usr/bin/env python3
"""
LinkedIn Selenium Automation - Unicode/Emoji Safe Version
Fixes ChromeDriver BMP and Windows terminal encoding issues
"""

import sys
import os
import time
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows terminal encoding issues
sys.stdout.reconfigure(encoding='utf-8')

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not installed. Run: pip install selenium")

load_dotenv()

# LinkedIn credentials from .env
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


def clean_text_for_selenium(text):
    """
    Clean text to prevent ChromeDriver BMP and Unicode errors
    Multiple strategies for maximum compatibility
    """
    if not text:
        return ""
    
    try:
        # Strategy 1: UTF-16 surrogate handling (recommended approach)
        cleaned = text.encode("utf-16", "surrogatepass").decode("utf-16")
        
        # Strategy 2: Remove non-BMP characters (characters outside Basic Multilingual Plane)
        # BMP range is U+0000 to U+FFFF
        cleaned = ''.join(char for char in cleaned if ord(char) <= 0xFFFF)
        
        # Strategy 3: Normalize Unicode to composed form
        cleaned = unicodedata.normalize('NFC', cleaned)
        
        # Strategy 4: Remove problematic emojis and symbols (optional - use if still having issues)
        # Uncomment the line below if you want to remove all emojis
        # cleaned = re.sub(r'[^\x00-\x7F\u00A0-\u024F\u1E00-\u1EFF\u2000-\u206F\u2070-\u209F\u20A0-\u20CF\u2100-\u214F\u2190-\u21FF\u2200-\u22FF]', '', cleaned)
        
        # Strategy 5: Replace common problematic characters
        replacements = {
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            '\u201C': '"',  # Left double quotation mark
            '\u201D': '"',  # Right double quotation mark
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
            '\u2026': '...', # Horizontal ellipsis
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        # Strategy 6: Ensure no null bytes or control characters
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\r\t')
        
        return cleaned.strip()
        
    except Exception as e:
        print(f"⚠️  Text cleaning error: {e}")
        # Fallback: ASCII-only version
        return ''.join(char for char in text if ord(char) < 128).strip()


def safe_send_keys_js(driver, element, text):
    """
    Safely send text using JavaScript injection instead of send_keys
    This bypasses ChromeDriver's BMP limitations
    """
    try:
        cleaned_text = clean_text_for_selenium(text)
        
        # Method 1: Set innerText (preserves line breaks)
        driver.execute_script("arguments[0].innerText = arguments[1];", element, cleaned_text)
        
        # Method 2: Trigger input events for better compatibility
        driver.execute_script("""
            var element = arguments[0];
            var text = arguments[1];
            
            // Clear existing content
            element.innerText = '';
            element.textContent = '';
            
            // Set new content
            element.innerText = text;
            
            // Trigger events
            var inputEvent = new Event('input', { bubbles: true });
            var changeEvent = new Event('change', { bubbles: true });
            
            element.dispatchEvent(inputEvent);
            element.dispatchEvent(changeEvent);
        """, element, cleaned_text)
        
        return True
        
    except Exception as e:
        print(f"❌ JavaScript injection failed: {e}")
        
        # Fallback: Traditional send_keys with cleaned text
        try:
            element.clear()
            element.send_keys(cleaned_text)
            return True
        except Exception as e2:
            print(f"❌ Fallback send_keys failed: {e2}")
            return False


class LinkedInPosterFixed:
    """
    LinkedIn automation with Unicode/emoji safety and robust error handling
    """
    
    def __init__(self, headless=False):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not installed. Run: pip install selenium")
        
        self.email = LINKEDIN_EMAIL
        self.password = LINKEDIN_PASSWORD
        self.driver = None
        self.headless = headless
        self.wait = None
        
        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials not found in .env file")
    
    def setup_driver(self):
        """Setup Chrome driver with enhanced options for stability"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Enhanced Chrome options for stability and Unicode support
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-iframes-during-prerender')
        chrome_options.add_argument('--disable-background-networking')
        
        # Unicode and encoding support
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument('--accept-lang=en-US,en')
        
        # Anti-detection measures
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Enhanced user agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Window size for consistency
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver initialized with Unicode support")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing Chrome driver: {e}")
            print("💡 Make sure Chrome and ChromeDriver are installed and updated")
            raise
    
    def login(self):
        """Enhanced login with better error handling"""
        try:
            print("🔐 Logging into LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            
            # Wait for page load
            self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            time.sleep(2)
            
            # Enter email with safe method
            email_field = self.driver.find_element(By.ID, "username")
            email_field.clear()
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete with multiple possible outcomes
            try:
                # Wait for either feed or challenge page
                self.wait.until(lambda driver: 
                    "feed" in driver.current_url or 
                    "mynetwork" in driver.current_url or
                    "challenge" in driver.current_url or
                    "checkpoint" in driver.current_url
                )
                
                current_url = self.driver.current_url
                
                if "feed" in current_url or "mynetwork" in current_url:
                    print("✅ Login successful!")
                    return True
                elif "challenge" in current_url or "checkpoint" in current_url:
                    print("⚠️  LinkedIn security challenge detected")
                    print("💡 Please complete the challenge manually and press Enter")
                    input("Press Enter after completing the challenge...")
                    
                    # Check again after manual intervention
                    if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                        print("✅ Login successful after challenge!")
                        return True
                    else:
                        print("❌ Login still failed after challenge")
                        return False
                else:
                    print(f"⚠️  Unexpected redirect: {current_url}")
                    return False
                    
            except TimeoutException:
                print("❌ Login timeout. Check credentials or network connection")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def create_post(self, content):
        """Create LinkedIn post with enhanced selector strategies and Unicode safety"""
        try:
            print("📝 Creating LinkedIn post...")
            print(f"📄 Content length: {len(content)} characters")
            
            # Clean content for safe processing
            safe_content = clean_text_for_selenium(content)
            print(f"📄 Cleaned content length: {len(safe_content)} characters")
            
            # Navigate to feed
            self.driver.get('https://www.linkedin.com/feed/')
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
            
            # Enhanced selectors for "Start a post" button
            start_post_selectors = [
                # Most common selectors
                "button[aria-label*='Start a post']",
                "button.share-box-feed-entry__trigger",
                "div.share-box-feed-entry__trigger",
                
                # Alternative selectors
                "button.artdeco-button--muted",
                "button[data-control-name='share_box_trigger']",
                ".share-box .artdeco-button",
                
                # XPath selectors
                "//button[contains(text(), 'Start a post')]",
                "//div[contains(@class, 'share-box')]//button",
                "//button[contains(@aria-label, 'Start a post')]",
                "//button[contains(@class, 'share-box')]"
            ]
            
            start_post_button = None
            for i, selector in enumerate(start_post_selectors):
                try:
                    print(f"🔍 Trying selector {i+1}/{len(start_post_selectors)}: {selector}")
                    
                    if selector.startswith('//'):
                        start_post_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        start_post_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ Found start post button with selector {i+1}")
                    break
                    
                except TimeoutException:
                    print(f"⏳ Selector {i+1} timed out")
                    continue
                except Exception as e:
                    print(f"❌ Selector {i+1} error: {e}")
                    continue
            
            if not start_post_button:
                print("❌ Could not find 'Start a post' button")
                self.driver.save_screenshot('error_start_post.png')
                print("📸 Screenshot saved: error_start_post.png")
                return False
            
            # Click start post button
            try:
                start_post_button.click()
            except Exception:
                # Try JavaScript click if regular click fails
                self.driver.execute_script("arguments[0].click();", start_post_button)
            
            time.sleep(3)
            
            # Enhanced selectors for text editor
            editor_selectors = [
                # Most common selectors
                "div.ql-editor[contenteditable='true']",
                "div[role='textbox']",
                "div.ql-editor",
                
                # Alternative selectors
                "div[contenteditable='true']",
                "div.editor-content",
                ".ql-container .ql-editor",
                
                # XPath selectors
                "//div[@contenteditable='true']",
                "//div[@role='textbox']",
                "//div[contains(@class, 'ql-editor')]"
            ]
            
            text_editor = None
            for i, selector in enumerate(editor_selectors):
                try:
                    print(f"🔍 Trying editor selector {i+1}/{len(editor_selectors)}: {selector}")
                    
                    if selector.startswith('//'):
                        text_editor = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        text_editor = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ Found text editor with selector {i+1}")
                    break
                    
                except TimeoutException:
                    print(f"⏳ Editor selector {i+1} timed out")
                    continue
                except Exception as e:
                    print(f"❌ Editor selector {i+1} error: {e}")
                    continue
            
            if not text_editor:
                print("❌ Could not find text editor")
                self.driver.save_screenshot('error_text_editor.png')
                print("📸 Screenshot saved: error_text_editor.png")
                return False
            
            # Click editor to focus
            try:
                text_editor.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", text_editor)
            
            time.sleep(1)
            
            # Enter content using safe method
            print("📝 Entering content using JavaScript injection...")
            if not safe_send_keys_js(self.driver, text_editor, safe_content):
                print("❌ Failed to enter content")
                return False
            
            time.sleep(2)
            
            # Enhanced selectors for Post button
            post_button_selectors = [
                # Most common selectors
                "button.share-actions__primary-action",
                "button[aria-label*='Post']",
                "button.artdeco-button--primary",
                
                # Alternative selectors
                "button[data-control-name='share.post']",
                ".share-actions button[type='submit']",
                "button.share-actions__primary-action.artdeco-button",
                
                # XPath selectors
                "//button[contains(text(), 'Post')]",
                "//button[@type='submit' and contains(@class, 'primary')]",
                "//button[contains(@class, 'share-actions__primary-action')]"
            ]
            
            post_button = None
            for i, selector in enumerate(post_button_selectors):
                try:
                    print(f"🔍 Trying post button selector {i+1}/{len(post_button_selectors)}: {selector}")
                    
                    if selector.startswith('//'):
                        post_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        post_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ Found post button with selector {i+1}")
                    break
                    
                except TimeoutException:
                    print(f"⏳ Post button selector {i+1} timed out")
                    continue
                except Exception as e:
                    print(f"❌ Post button selector {i+1} error: {e}")
                    continue
            
            if not post_button:
                print("❌ Could not find Post button")
                self.driver.save_screenshot('error_post_button.png')
                print("📸 Screenshot saved: error_post_button.png")
                return False
            
            # Click post button
            try:
                post_button.click()
            except Exception:
                # Try JavaScript click if regular click fails
                self.driver.execute_script("arguments[0].click();", post_button)
            
            print("✅ Post button clicked!")
            time.sleep(5)
            
            # Verify post was created (optional)
            try:
                # Look for success indicators
                success_indicators = [
                    "//div[contains(text(), 'Post successful')]",
                    "//div[contains(text(), 'Your post was shared')]",
                    "//span[contains(text(), 'Posted')]"
                ]
                
                for indicator in success_indicators:
                    try:
                        self.driver.find_element(By.XPATH, indicator)
                        print("✅ Post success confirmed!")
                        break
                    except:
                        continue
                        
            except Exception:
                pass  # Success verification is optional
            
            print("✅ Post created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating post: {e}")
            self.driver.save_screenshot('error_general.png')
            print("📸 Screenshot saved: error_general.png")
            print(f"📄 Current URL: {self.driver.current_url}")
            return False
    
    def extract_content_from_file(self, filepath):
        """Extract and clean content from markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract content section
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
            
            # Join content
            final_content = '\n\n'.join(post_content)
            
            if not final_content:
                print("⚠️  No content found in file")
                return None
            
            return final_content
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None
    
    def post_from_file(self, filepath):
        """Read post content from file and post to LinkedIn"""
        content = self.extract_content_from_file(filepath)
        if content is None:
            return False
        
        print(f"📄 Original content length: {len(content)} characters")
        return self.create_post(content)
    
    def close(self):
        """Close browser safely"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔒 Browser closed")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")


def post_to_linkedin_safe(filepath, headless=False):
    """
    Main function to safely post to LinkedIn with Unicode support
    """
    poster = None
    
    try:
        print("=" * 70)
        print("🔵 LinkedIn Auto-Poster (Unicode Safe)")
        print("=" * 70)
        print()
        
        # Initialize poster
        poster = LinkedInPosterFixed(headless=headless)
        
        if not poster.setup_driver():
            return False
        
        # Login
        if not poster.login():
            print("❌ Login failed. Check credentials in .env file")
            return False
        
        # Post content
        if poster.post_from_file(filepath):
            print()
            print("=" * 70)
            print("✅ Successfully posted to LinkedIn!")
            print("=" * 70)
            return True
        else:
            print("❌ Failed to post")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    finally:
        if poster:
            time.sleep(3)  # Wait to see result
            poster.close()


def main():
    """Test the LinkedIn poster with file argument or auto-detection"""
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return
    else:
        # Find latest unposted LinkedIn post
        posted_folder = Path('03_Posted/History')
        if not posted_folder.exists():
            print("❌ Posted folder not found: 03_Posted/History/")
            return
        
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        unposted = [p for p in posts if not p.name.startswith('POSTED_')]
        
        if not unposted:
            print("✅ No unposted LinkedIn posts found")
            print("💡 All posts are already posted or no posts exist")
            return
        
        # Get latest unposted
        filepath = max(unposted, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using latest unposted: {filepath.name}")
    
    # Test content cleaning
    test_content = "Test post with emojis 🚀 and unicode characters: café, naïve, résumé"
    cleaned = clean_text_for_selenium(test_content)
    print(f"🧪 Test cleaning: '{test_content}' → '{cleaned}'")
    print()
    
    # Post to LinkedIn
    success = post_to_linkedin_safe(str(filepath), headless=False)
    
    if success:
        # Mark as posted
        new_name = f"POSTED_{filepath.name}"
        new_path = filepath.parent / new_name
        filepath.rename(new_path)
        print(f"✅ File renamed to: {new_name}")
    else:
        print("❌ Posting failed - file not renamed")


if __name__ == "__main__":
    main()