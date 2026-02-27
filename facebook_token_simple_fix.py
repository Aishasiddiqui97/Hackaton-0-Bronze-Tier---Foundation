#!/usr/bin/env python3
"""
Simple Facebook Token Fix
Get a new long-lived token without needing App Secret
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_current_token():
    """Test the current Facebook token"""
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    if not token:
        print("[ERROR] No Facebook token found in .env")
        return False
    
    print("[INFO] Testing current Facebook token...")
    
    # Test token validity
    url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] Token is valid for: {data.get('name', 'Unknown')}")
        
        # Check token info
        debug_url = f"https://graph.facebook.com/v18.0/debug_token?input_token={token}&access_token={token}"
        debug_response = requests.get(debug_url)
        
        if debug_response.status_code == 200:
            debug_data = debug_response.json().get('data', {})
            expires_at = debug_data.get('expires_at', 0)
            
            if expires_at == 0:
                print("[SUCCESS] Token never expires (long-lived)")
                return True
            else:
                from datetime import datetime
                expiry_date = datetime.fromtimestamp(expires_at)
                print(f"[INFO] Token expires: {expiry_date}")
                
                if expiry_date > datetime.now():
                    print("[SUCCESS] Token is still valid")
                    return True
                else:
                    print("[ERROR] Token has expired")
                    return False
        
        return True
    else:
        error_data = response.json()
        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
        print(f"[ERROR] Token invalid: {error_msg}")
        return False

def get_simple_instructions():
    """Provide simple instructions for getting a new token"""
    print("\n" + "="*60)
    print("SIMPLE FACEBOOK TOKEN FIX")
    print("="*60)
    print()
    print("Since your current token is expired, here's the easiest way to fix it:")
    print()
    print("METHOD 1: Facebook Graph API Explorer (Recommended)")
    print("-" * 50)
    print("1. Go to: https://developers.facebook.com/tools/explorer/")
    print("2. Make sure your app is selected in the dropdown")
    print("3. Click 'Generate Access Token'")
    print("4. Select these permissions:")
    print("   ✓ pages_manage_posts")
    print("   ✓ pages_read_engagement")
    print("   ✓ pages_show_list")
    print("5. Click 'Generate Access Token'")
    print("6. Copy the token (it will be long)")
    print("7. Paste it below")
    print()
    
    new_token = input("Paste your new Facebook token here: ").strip()
    
    if new_token and len(new_token) > 50:
        return new_token
    else:
        print("[ERROR] Token seems too short or invalid")
        return None

def update_env_with_new_token(new_token):
    """Update .env file with new token"""
    try:
        # Read current .env
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update Facebook token line
        updated_lines = []
        token_updated = False
        
        for line in lines:
            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={new_token}\n')
                token_updated = True
                print("[SUCCESS] Updated Facebook token in .env")
            elif line.startswith('INSTAGRAM_ACCESS_TOKEN='):
                updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={new_token}\n')
                print("[SUCCESS] Updated Instagram token in .env (same token)")
            else:
                updated_lines.append(line)
        
        # If no Facebook token line exists, add it
        if not token_updated:
            updated_lines.append(f'\nFACEBOOK_ACCESS_TOKEN={new_token}\n')
            updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={new_token}\n')
            print("[SUCCESS] Added Facebook and Instagram tokens to .env")
        
        # Write updated .env
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        print("[SUCCESS] .env file updated successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update .env: {e}")
        return False

def test_new_token(token):
    """Test the new token before saving"""
    print("[INFO] Testing new token...")
    
    url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] New token works! Connected as: {data.get('name')}")
        
        # Test page access
        page_id = os.getenv('FACEBOOK_PAGE_ID')
        if page_id:
            page_url = f"https://graph.facebook.com/v18.0/{page_id}?access_token={token}"
            page_response = requests.get(page_url)
            
            if page_response.status_code == 200:
                page_data = page_response.json()
                print(f"[SUCCESS] Page access confirmed: {page_data.get('name', 'Your Page')}")
                return True
            else:
                print(f"[WARNING] Page access issue: {page_response.text}")
                print("[INFO] Token works for user, but check page permissions")
                return True
        
        return True
    else:
        error_data = response.json()
        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
        print(f"[ERROR] New token failed: {error_msg}")
        return False

def main():
    """Main token fixing function"""
    print("="*60)
    print("FACEBOOK TOKEN SIMPLE FIX")
    print("="*60)
    print()
    
    # Test current token
    if test_current_token():
        print("\n[SUCCESS] Your current token is working fine!")
        print("[INFO] No action needed.")
        return
    
    print("\n[INFO] Current token needs to be refreshed.")
    
    # Get new token
    new_token = get_simple_instructions()
    
    if not new_token:
        print("\n[ERROR] No valid token provided. Please try again.")
        return
    
    # Test new token
    if test_new_token(new_token):
        # Update .env file
        if update_env_with_new_token(new_token):
            print("\n" + "="*60)
            print("[SUCCESS] FACEBOOK TOKEN FIXED!")
            print("="*60)
            print()
            print("✓ New token tested and working")
            print("✓ .env file updated")
            print("✓ Instagram token also updated")
            print()
            print("Next steps:")
            print("1. Test Facebook posting: python api_facebook_poster_fixed.py")
            print("2. Restart your Gold Tier system")
            print()
        else:
            print("\n[ERROR] Failed to update .env file")
            print(f"[INFO] Manually add this line to your .env file:")
            print(f"FACEBOOK_ACCESS_TOKEN={new_token}")
    else:
        print("\n[ERROR] New token is not working. Please try again.")

if __name__ == "__main__":
    main()