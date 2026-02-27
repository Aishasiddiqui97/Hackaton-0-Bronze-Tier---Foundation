#!/usr/bin/env python3
"""
Facebook Page Token Guide
Step-by-step guide to get the correct Page Access Token
"""

import os
import requests

def test_token(token, token_type="Unknown"):
    """Test any token"""
    try:
        url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            name = data.get('name', 'Unknown')
            print(f"[SUCCESS] {token_type} token works! Connected as: {name}")
            return True
        else:
            print(f"[ERROR] {token_type} token failed")
            return False
    except Exception as e:
        print(f"[ERROR] {token_type} token error: {e}")
        return False

def main():
    """Guide user through getting Page Access Token"""
    print("="*70)
    print("FACEBOOK PAGE ACCESS TOKEN - STEP BY STEP GUIDE")
    print("="*70)
    print()
    
    print("The issue: You need a PAGE ACCESS TOKEN, not a User Access Token")
    print()
    print("STEP 1: Go to Facebook Graph API Explorer")
    print("-" * 50)
    print("1. Open: https://developers.facebook.com/tools/explorer/")
    print("2. Make sure your app is selected")
    print()
    
    print("STEP 2: Change Token Type (IMPORTANT!)")
    print("-" * 50)
    print("1. Look for 'Access Token' dropdown (currently shows 'User Token')")
    print("2. Click it and change to 'Page Access Token'")
    print("3. Select your Facebook page from the list")
    print("4. If no pages appear, you need to create a Facebook page first")
    print()
    
    print("STEP 3: Generate Page Token")
    print("-" * 50)
    print("1. Click 'Generate Access Token'")
    print("2. Select permissions:")
    print("   ✓ pages_manage_posts")
    print("   ✓ pages_read_engagement")
    print("3. Click 'Generate Access Token'")
    print("4. Copy the token (starts with 'EAAVLp...')")
    print()
    
    print("STEP 4: Test Your Page Token")
    print("-" * 50)
    token = input("Paste your PAGE ACCESS TOKEN here: ").strip()
    
    if not token:
        print("[ERROR] No token provided")
        return
    
    if len(token) < 50:
        print("[ERROR] Token too short - make sure you copied the full token")
        return
    
    print(f"\n[INFO] Testing page token (length: {len(token)} chars)...")
    
    if test_token(token, "Page"):
        # Test posting capability
        page_id = input("\nEnter your Facebook Page ID (numbers only): ").strip()
        
        if page_id:
            print(f"[INFO] Testing posting to page {page_id}...")
            
            try:
                url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
                test_payload = {
                    "message": "Test from AI Employee - please ignore",
                    "access_token": token
                }
                
                response = requests.post(url, data=test_payload)
                
                if response.status_code == 200:
                    post_data = response.json()
                    post_id = post_data.get('id')
                    print(f"[SUCCESS] Posting works! Test post ID: {post_id}")
                    
                    # Delete test post
                    delete_url = f"https://graph.facebook.com/v18.0/{post_id}?access_token={token}"
                    requests.delete(delete_url)
                    print("[INFO] Test post deleted")
                    
                    # Update .env
                    try:
                        with open('.env', 'r') as f:
                            content = f.read()
                        
                        lines = content.split('\n')
                        updated_lines = []
                        
                        for line in lines:
                            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                                updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={token}')
                            elif line.startswith('FACEBOOK_PAGE_ID='):
                                updated_lines.append(f'FACEBOOK_PAGE_ID={page_id}')
                            else:
                                updated_lines.append(line)
                        
                        with open('.env', 'w') as f:
                            f.write('\n'.join(updated_lines))
                        
                        print("\n" + "="*70)
                        print("SUCCESS! FACEBOOK PAGE TOKEN CONFIGURED!")
                        print("="*70)
                        print()
                        print("✓ Page Access Token working")
                        print("✓ Posting capability confirmed")
                        print("✓ .env file updated")
                        print()
                        print("Test Facebook posting:")
                        print("  python api_facebook_poster_fixed.py")
                        print()
                        
                    except Exception as e:
                        print(f"[ERROR] Could not update .env: {e}")
                        print(f"\nManual update needed:")
                        print(f"FACEBOOK_ACCESS_TOKEN={token}")
                        print(f"FACEBOOK_PAGE_ID={page_id}")
                
                else:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown')
                    print(f"[ERROR] Posting failed: {error_msg}")
                    print("\nPossible issues:")
                    print("1. Wrong Page ID")
                    print("2. No admin rights to page")
                    print("3. Missing permissions")
                    
            except Exception as e:
                print(f"[ERROR] Test failed: {e}")
        
    else:
        print("\n[ERROR] Page token not working")
        print("\nTroubleshooting:")
        print("1. Make sure you selected 'Page Access Token' (not User Token)")
        print("2. Select the correct page")
        print("3. Include required permissions")
        print("4. Make sure you're admin of the page")

if __name__ == "__main__":
    main()