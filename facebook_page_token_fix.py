#!/usr/bin/env python3
"""
Facebook Page Token Fix
Get the correct Page Access Token for posting
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_user_pages(user_token):
    """Get list of pages the user manages"""
    try:
        url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={user_token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get('data', [])
            
            if pages:
                print(f"[SUCCESS] Found {len(pages)} page(s) you manage:")
                print()
                
                for i, page in enumerate(pages, 1):
                    page_id = page.get('id')
                    page_name = page.get('name')
                    page_token = page.get('access_token')
                    
                    print(f"{i}. {page_name}")
                    print(f"   ID: {page_id}")
                    print(f"   Token: {page_token[:50]}...")
                    print()
                
                return pages
            else:
                print("[ERROR] No pages found. You need to:")
                print("1. Create a Facebook page")
                print("2. Make sure you're an admin of the page")
                return []
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"[ERROR] Failed to get pages: {error_msg}")
            return []
            
    except Exception as e:
        print(f"[ERROR] Exception getting pages: {e}")
        return []

def test_page_posting(page_id, page_token):
    """Test if we can post to a specific page"""
    try:
        # Test with a simple message
        url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        
        test_payload = {
            "message": "Test post from AI Employee System - please ignore",
            "access_token": page_token
        }
        
        print(f"[INFO] Testing posting to page {page_id}...")
        response = requests.post(url, data=test_payload)
        
        if response.status_code == 200:
            post_data = response.json()
            post_id = post_data.get('id')
            print(f"[SUCCESS] Test post successful! Post ID: {post_id}")
            
            # Delete the test post
            delete_url = f"https://graph.facebook.com/v18.0/{post_id}?access_token={page_token}"
            delete_response = requests.delete(delete_url)
            
            if delete_response.status_code == 200:
                print("[INFO] Test post deleted successfully")
            
            return True
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"[ERROR] Test post failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception testing post: {e}")
        return False

def update_env_with_page_token(page_id, page_token):
    """Update .env with correct page ID and token"""
    try:
        # Read current .env
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update lines
        updated_lines = []
        
        for line in lines:
            if line.startswith('FACEBOOK_ACCESS_TOKEN='):
                updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={page_token}\n')
            elif line.startswith('FACEBOOK_PAGE_ID='):
                updated_lines.append(f'FACEBOOK_PAGE_ID={page_id}\n')
            elif line.startswith('INSTAGRAM_ACCESS_TOKEN='):
                updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={page_token}\n')
            else:
                updated_lines.append(line)
        
        # Write back
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        print("[SUCCESS] .env file updated with page token!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update .env: {e}")
        return False

def main():
    """Main page token fix function"""
    print("="*60)
    print("FACEBOOK PAGE TOKEN FIX")
    print("="*60)
    print()
    
    # Get current user token
    user_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    if not user_token:
        print("[ERROR] No Facebook token found in .env")
        print("[INFO] Run facebook_quick_token_fix.py first")
        return
    
    print("[INFO] Getting your Facebook pages...")
    
    # Get user's pages
    pages = get_user_pages(user_token)
    
    if not pages:
        print("\n[ERROR] No pages found or accessible.")
        print("\nTo fix this:")
        print("1. Create a Facebook page if you don't have one")
        print("2. Make sure you're an admin of the page")
        print("3. In Graph API Explorer, use 'Page Access Token' instead of 'User Access Token'")
        return
    
    # Let user choose page
    if len(pages) == 1:
        selected_page = pages[0]
        print(f"[INFO] Using your only page: {selected_page['name']}")
    else:
        print("Which page do you want to use for posting?")
        try:
            choice = int(input("Enter page number: ")) - 1
            if 0 <= choice < len(pages):
                selected_page = pages[choice]
            else:
                print("[ERROR] Invalid choice")
                return
        except ValueError:
            print("[ERROR] Please enter a number")
            return
    
    page_id = selected_page['id']
    page_name = selected_page['name']
    page_token = selected_page['access_token']
    
    print(f"\n[INFO] Selected page: {page_name} (ID: {page_id})")
    
    # Test posting to the page
    if test_page_posting(page_id, page_token):
        # Update .env file
        if update_env_with_page_token(page_id, page_token):
            print("\n" + "="*60)
            print("SUCCESS! FACEBOOK PAGE TOKEN FIXED!")
            print("="*60)
            print()
            print(f"✓ Page: {page_name}")
            print(f"✓ Page ID: {page_id}")
            print("✓ Page token configured")
            print("✓ Test post successful")
            print("✓ .env file updated")
            print()
            print("Test Facebook posting now:")
            print("  python api_facebook_poster_fixed.py")
            print()
        else:
            print(f"\n[INFO] Manual update needed:")
            print(f"Update your .env file:")
            print(f"FACEBOOK_PAGE_ID={page_id}")
            print(f"FACEBOOK_ACCESS_TOKEN={page_token}")
    else:
        print(f"\n[ERROR] Cannot post to page: {page_name}")
        print("This might be because:")
        print("1. You don't have admin rights to the page")
        print("2. The page doesn't allow API posting")
        print("3. Your app needs additional permissions")

if __name__ == "__main__":
    main()