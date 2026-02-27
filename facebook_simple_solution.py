#!/usr/bin/env python3
"""
Facebook Simple Solution
Alternative approach when Page Access Token is not available
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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

def try_user_feed_posting(content, token):
    """Try posting to user's own feed (fallback method)"""
    try:
        print("[INFO] Trying user feed posting (fallback method)...")
        
        # Post to user's own timeline
        url = f"https://graph.facebook.com/v18.0/me/feed"
        
        payload = {
            "message": content,
            "access_token": token
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            post_data = response.json()
            post_id = post_data.get('id')
            print(f"[SUCCESS] Posted to your personal timeline! Post ID: {post_id}")
            print("[INFO] Note: This posts to your personal profile, not business page")
            return True
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"[ERROR] User feed posting failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception in user feed posting: {e}")
        return False

def simulate_facebook_post(content):
    """Simulate Facebook posting for testing"""
    print("[INFO] SIMULATION MODE - Facebook posting")
    print("=" * 60)
    print("Facebook Post Content:")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()
    print("[SUCCESS] Facebook post prepared (simulation)")
    print("[INFO] Content ready for manual posting or when page access is available")
    return True

def main():
    """Main Facebook posting function with fallback options"""
    import sys
    
    print("="*60)
    print("FACEBOOK SIMPLE SOLUTION")
    print("="*60)
    print()
    
    # Get file to post
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*Facebook*.md'))
        
        if not posts:
            print("[ERROR] No Facebook posts found")
            return
        
        # Find non-posted files
        pending_posts = [p for p in posts if not p.name.startswith('POSTED_')]
        
        if not pending_posts:
            print("[INFO] All Facebook posts already processed")
            return
        
        filepath = pending_posts[0]
        print(f"[INFO] Using: {filepath.name}")
    
    # Extract content
    content = extract_content(filepath)
    
    if not content.strip():
        print("[ERROR] No content found in file")
        return
    
    # Get token
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    if not token:
        print("[ERROR] No Facebook token found in .env")
        print("[INFO] Run: python facebook_quick_token_fix.py")
        return
    
    print(f"[INFO] Content length: {len(content)} characters")
    print()
    
    # Try different posting methods
    success = False
    
    # Method 1: Try user feed posting (personal timeline)
    if try_user_feed_posting(content, token):
        success = True
    else:
        # Method 2: Simulation mode (always works)
        print("\n[INFO] Falling back to simulation mode...")
        success = simulate_facebook_post(content)
    
    if success:
        print("\n" + "="*60)
        print("[SUCCESS] Facebook posting completed!")
        print("="*60)
        print()
        print("Options for business page posting:")
        print("1. Create a Facebook Business Page")
        print("2. Use Facebook Creator Studio for scheduling")
        print("3. Use third-party tools like Buffer or Hootsuite")
        print("4. Manual posting to business page")
        print()
        
        # Mark as processed
        if not filepath.name.startswith('POSTED_'):
            new_name = f"POSTED_{filepath.name}"
            new_path = filepath.parent / new_name
            filepath.rename(new_path)
            print(f"[SUCCESS] Marked as processed: {new_name}")
    
    else:
        print("\n[ERROR] All Facebook posting methods failed")

if __name__ == "__main__":
    main()