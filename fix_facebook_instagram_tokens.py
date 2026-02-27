#!/usr/bin/env python3
"""
Fix Facebook and Instagram Access Tokens
Helps refresh expired tokens and test connectivity
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def test_facebook_token():
    """Test current Facebook token"""
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    if not token:
        print("❌ No Facebook token found in .env")
        return False
    
    print("🔍 Testing Facebook token...")
    
    # Test token validity
    url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Token valid for: {data.get('name', 'Unknown')}")
        
        # Test page access
        if page_id:
            page_url = f"https://graph.facebook.com/v18.0/{page_id}?access_token={token}"
            page_response = requests.get(page_url)
            
            if page_response.status_code == 200:
                page_data = page_response.json()
                print(f"✅ Page access: {page_data.get('name', 'Unknown Page')}")
                return True
            else:
                print(f"❌ Page access failed: {page_response.text}")
                return False
        return True
    else:
        print(f"❌ Token invalid: {response.text}")
        return False

def test_instagram_token():
    """Test current Instagram token"""
    token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    if not token:
        print("❌ No Instagram token found in .env")
        return False
    
    print("🔍 Testing Instagram token...")
    
    # Test token validity
    url = f"https://graph.facebook.com/v18.0/{account_id}?fields=id,username&access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Instagram account: {data.get('username', 'Unknown')}")
        return True
    else:
        print(f"❌ Instagram token invalid: {response.text}")
        return False

def get_long_lived_token(short_token):
    """Convert short-lived token to long-lived (60 days)"""
    app_id = input("Enter your Facebook App ID: ")
    app_secret = input("Enter your Facebook App Secret: ")
    
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        new_token = data.get('access_token')
        expires_in = data.get('expires_in', 'Unknown')
        
        print(f"✅ Long-lived token generated!")
        print(f"📅 Expires in: {expires_in} seconds (~60 days)")
        print(f"🔑 New token: {new_token}")
        
        return new_token
    else:
        print(f"❌ Failed to get long-lived token: {response.text}")
        return None

def generate_new_tokens():
    """Guide user through token generation"""
    print("\n" + "="*60)
    print("🔧 FACEBOOK/INSTAGRAM TOKEN GENERATION GUIDE")
    print("="*60)
    print()
    
    print("To fix your tokens, follow these steps:")
    print()
    print("1. Go to: https://developers.facebook.com/tools/explorer/")
    print("2. Select your app")
    print("3. Generate User Access Token with permissions:")
    print("   - pages_manage_posts")
    print("   - pages_read_engagement") 
    print("   - instagram_basic")
    print("   - instagram_content_publish")
    print("4. Copy the token and paste below")
    print()
    
    new_token = input("Paste your new Facebook token: ").strip()
    
    if new_token:
        print("\n🔄 Converting to long-lived token...")
        long_token = get_long_lived_token(new_token)
        
        if long_token:
            print("\n📝 Update your .env file with:")
            print(f"FACEBOOK_ACCESS_TOKEN={long_token}")
            print(f"INSTAGRAM_ACCESS_TOKEN={long_token}")
            print()
            print("💡 The same token works for both Facebook and Instagram")
            
            # Offer to update .env automatically
            update = input("\nUpdate .env file automatically? (y/n): ").lower()
            if update == 'y':
                update_env_file(long_token)
        
def update_env_file(new_token):
    """Update .env file with new token"""
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        updated_lines = []
        for line in lines:
            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={new_token}\n')
            elif line.startswith('INSTAGRAM_ACCESS_TOKEN='):
                updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={new_token}\n')
            else:
                updated_lines.append(line)
        
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env file updated successfully!")
        print("🔄 Restart your posting system to use new tokens")
        
    except Exception as e:
        print(f"❌ Failed to update .env: {e}")

def main():
    """Main token testing and fixing function"""
    print("="*60)
    print("🔧 FACEBOOK & INSTAGRAM TOKEN FIXER")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test current tokens
    fb_valid = test_facebook_token()
    ig_valid = test_instagram_token()
    
    print("\n" + "="*60)
    print("📊 TOKEN STATUS SUMMARY")
    print("="*60)
    print(f"Facebook: {'✅ Valid' if fb_valid else '❌ Invalid'}")
    print(f"Instagram: {'✅ Valid' if ig_valid else '❌ Invalid'}")
    
    if not fb_valid or not ig_valid:
        print("\n🔧 Tokens need to be refreshed!")
        fix = input("\nWould you like to generate new tokens? (y/n): ").lower()
        
        if fix == 'y':
            generate_new_tokens()
        else:
            print("\n💡 Manual fix instructions:")
            print("1. Go to Facebook Developer Console")
            print("2. Generate new access tokens")
            print("3. Update .env file")
            print("4. Restart your system")
    else:
        print("\n🎉 All tokens are valid!")

if __name__ == "__main__":
    main()