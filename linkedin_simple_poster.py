#!/usr/bin/env python3
"""
Simple LinkedIn Poster - Works with LinkedIn's current UI
Uses improved Selenium with explicit waits and better selectors
"""

import os
import time
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
    from selenium.webdriver.common.action_chains import ActionChains
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

load_dotenv()

LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


def post_to_linkedin_simple(content):
    """Simple LinkedIn posting with better reliability"""
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed. Run: pip install selenium")
        return False
    
    driver = None
    
    try:
        print("=" * 60)
        print("LinkedIn Auto-Poster (Simple Mode)")
        print("=" * 60)
        print()
        
        # Setup Chrome
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Browser started")
        
        # Login
        print("🔐 Logging in...")
        driver.get('https://www.linkedin.com/login')
        time.sleep(3)
        
        # Email
        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(LINKEDIN_EMAIL)
        
        # Password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(LINKEDIN_PASSWORD)
        
        # Login button
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        time.sleep(8)  # Wait for login
        
        print("✅ Logged in")
        
        # Go to feed
        print("📱 Opening feed...")
        driver.get('https://www.linkedin.com/feed/')
        time.sleep(5)
        
        # Method 1: Try clicking the share box
        try:
            print("🔍 Looking for share box...")
            share_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-box-feed-entry__trigger')]"))
            )
            share_box.click()
            print("✅ Clicked share box")
            time.sleep(3)
        except:
            # Method 2: Try alternative selector
            try:
                print("🔍 Trying alternative selector...")
                share_box = driver.find_element(By.XPATH, "//span[contains(text(), 'Start a post')]/..")
                share_box.click()
                print("✅ Clicked share box (alternative)")
                time.sleep(3)
            except:
                print("❌ Could not find share box")
                driver.save_screenshot('error_share_box.png')
                return False
        
        # Find editor and enter content
        try:
            print("📝 Entering content...")
            
            # Wait for editor to appear
            editor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor[contenteditable='true']"))
            )
            
            # Click editor
            editor.click()
            time.sleep(1)
            
            # Type content slowly (more human-like)
            for char in content:
                editor.send_keys(char)
                if char in ['.', '!', '?', '\n']:
                    time.sleep(0.1)
            
            print("✅ Content entered")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error entering content: {e}")
            driver.save_screenshot('error_content.png')
            return False
        
        # Click Post button
        try:
            print("📤 Clicking Post button...")
            
            # Find and click Post button
            post_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]"))
            )
            post_btn.click()
            
            print("✅ Post button clicked")
            time.sleep(5)
            
            print()
            print("=" * 60)
            print("✅ Successfully posted to LinkedIn!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Error clicking Post button: {e}")
            driver.save_screenshot('error_post_button.png')
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if driver:
            driver.save_screenshot('error_general.png')
        return False
        
    finally:
        if driver:
            time.sleep(3)
            driver.quit()
            print("🔒 Browser closed")


def extract_content_from_file(filepath):
    """Extract post content from markdown file"""
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
        elif in_content and line.strip():
            # Remove emoji and markdown formatting
            clean_line = line.strip()
            if not clean_line.startswith('#'):
                post_lines.append(clean_line)
    
    return '\n\n'.join(post_lines)


def main():
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Find latest post
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        
        if not posts:
            print("❌ No LinkedIn posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    # Extract content
    content = extract_content_from_file(filepath)
    
    print(f"📄 Content ({len(content)} chars):")
    print("-" * 60)
    print(content[:200] + "..." if len(content) > 200 else content)
    print("-" * 60)
    print()
    
    # Post
    success = post_to_linkedin_simple(content)
    
    if success:
        print("\n✅ All done!")
    else:
        print("\n❌ Posting failed")


if __name__ == "__main__":
    main()
