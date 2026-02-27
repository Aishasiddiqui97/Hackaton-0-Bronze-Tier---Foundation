"""
Test LinkedIn Login - Debug Version
"""
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

load_dotenv()

LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

print("=" * 60)
print("LinkedIn Login Test")
print("=" * 60)
print()

# Check credentials
if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    print("❌ LinkedIn credentials not found in .env file")
    print("Please add:")
    print("  LINKEDIN_EMAIL=your_email")
    print("  LINKEDIN_PASSWORD=your_password")
    exit(1)

print(f"✅ Email found: {LINKEDIN_EMAIL}")
print(f"✅ Password found: {'*' * len(LINKEDIN_PASSWORD)}")
print()

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

print("🚀 Starting Chrome browser...")
driver = webdriver.Chrome(options=chrome_options)

try:
    print("🌐 Opening LinkedIn login page...")
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)
    
    print("📝 Entering email...")
    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.clear()
    email_field.send_keys(LINKEDIN_EMAIL)
    time.sleep(1)
    
    print("🔐 Entering password...")
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(LINKEDIN_PASSWORD)
    time.sleep(1)
    
    print("🔘 Clicking login button...")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    print("⏳ Waiting for login (10 seconds)...")
    time.sleep(10)
    
    current_url = driver.current_url
    print(f"\n📍 Current URL: {current_url}")
    
    if "feed" in current_url or "mynetwork" in current_url or "linkedin.com/in/" in current_url:
        print("\n✅ LOGIN SUCCESSFUL!")
        print("🎉 Your credentials are working!")
    elif "checkpoint" in current_url or "challenge" in current_url:
        print("\n⚠️  SECURITY CHECKPOINT DETECTED")
        print("LinkedIn is asking for verification.")
        print("This is normal for automated logins.")
        print("\n💡 Solutions:")
        print("1. Complete verification manually in the browser")
        print("2. Login manually once from this computer")
        print("3. Use LinkedIn API instead (if available)")
        print("\n⏳ Keeping browser open for 60 seconds...")
        print("Complete the verification if needed...")
        time.sleep(60)
    else:
        print("\n❌ LOGIN FAILED")
        print("Possible reasons:")
        print("1. Wrong email or password")
        print("2. LinkedIn security measures")
        print("3. Account locked or restricted")
        print("\n📸 Taking screenshot...")
        driver.save_screenshot('login_test_failed.png')
        print("Screenshot saved: login_test_failed.png")
    
    print("\n⏳ Keeping browser open for 10 more seconds...")
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    driver.save_screenshot('login_test_error.png')
    print("Screenshot saved: login_test_error.png")

finally:
    print("\n🔒 Closing browser...")
    driver.quit()
    print("✅ Test complete!")

print("\n" + "=" * 60)
print("Test finished. Check the output above.")
print("=" * 60)
