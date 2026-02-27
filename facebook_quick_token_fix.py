#!/usr/bin/env python3
"""
Facebook Quick Token Fix
Easiest way to get a working Facebook token
"""

import os
import requests

def test_token(token):
    """Test if a token works"""
    try:
        url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            name = data.get('name', 'Unknown')
            print(f"[SUCCESS] Token works! Connected as: {name}")
            return True
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"[ERROR] Token failed: {error_msg}")
            return False
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")
        return False

def update_env_file(token):
    """Update .env file with new token"""
    try:
        # Read current .env
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace Facebook token
        lines = content.split('\n')
        updated_lines = []
        fb_updated = False
        ig_updated = False
        
        for line in lines:
            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={token}')
                fb_updated = True
            elif line.startswith('INSTAGRAM_ACCESS_TOKEN='):
                updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={token}')
                ig_updated = True
            else:
                updated_lines.append(line)
        
        # Add tokens if they don't exist
        if not fb_updated:
            updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={token}')
        if not ig_updated:
            updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={token}')
        
        # Write back to file
        with open('.env', 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print("[SUCCESS] .env file updated!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update .env: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("FACEBOOK QUICK TOKEN FIX")
    print("="*60)
    print()
    
    print("STEP 1: Get a new Facebook token")
    print("-" * 40)
    print("1. Open: https://developers.facebook.com/tools/explorer/")
    print("2. Select your Facebook app from dropdown")
    print("3. Click 'Generate Access Token' button")
    print("4. Select permissions: pages_manage_posts, pages_read_engagement")
    print("5. Click 'Generate Access Token'")
    print("6. Copy the ENTIRE token (it's very long)")
    print()
    
    print("STEP 2: Paste your token")
    print("-" * 40)
    print("Paste your Facebook access token below:")
    print("(It should start with something like 'EAAVLp...' and be very long)")
    print()
    
    # Get token from user
    token = input("Token: ").strip()
    
    if not token:
        print("[ERROR] No token provided")
        return
    
    if len(token) < 50:
        print("[ERROR] Token seems too short. Make sure you copied the full token.")
        return
    
    print(f"\n[INFO] Testing token (length: {len(token)} chars)...")
    
    # Test the token
    if test_token(token):
        # Update .env file
        if update_env_file(token):
            print("\n" + "="*60)
            print("SUCCESS! FACEBOOK TOKEN FIXED!")
            print("="*60)
            print()
            print("✓ Token tested and working")
            print("✓ .env file updated")
            print("✓ Ready for Facebook posting")
            print()
            print("Test it now:")
            print("  python api_facebook_poster_fixed.py")
            print()
        else:
            print(f"\n[INFO] Manual update needed:")
            print(f"Add this to your .env file:")
            print(f"FACEBOOK_ACCESS_TOKEN={token}")
    else:
        print("\n[ERROR] Token is not working. Please:")
        print("1. Make sure you copied the COMPLETE token")
        print("2. Check that your Facebook app has the right permissions")
        print("3. Try generating a new token")

if __name__ == "__main__":
    main()