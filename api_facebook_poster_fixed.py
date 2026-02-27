#!/usr/bin/env python3
"""
Facebook API Poster - Fixed for Windows Console
More reliable than browser automation
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')


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


def extract_page_id_from_url(url):
    """Extract numeric page ID from Facebook URL"""
    # URL format: https://www.facebook.com/profile.php?id=61588226203596
    if 'id=' in url:
        return url.split('id=')[1].split('&')[0]
    return None


def post_to_facebook_api(content):
    """Post to Facebook using Graph API"""
    
    if not FACEBOOK_ACCESS_TOKEN:
        print("[ERROR] Facebook Access Token not found in .env")
        return False
    
    try:
        print("=" * 60)
        print("Facebook API Poster")
        print("=" * 60)
        print()
        
        # Extract page ID from URL if needed
        page_id = FACEBOOK_PAGE_ID
        if page_id and page_id.startswith('http'):
            page_id = extract_page_id_from_url(page_id)
        
        if not page_id:
            print("[ERROR] Facebook Page ID not found")
            return False
        
        print(f"[INFO] Content ({len(content)} chars):")
        print("-" * 60)
        print(content)
        print("-" * 60)
        print()
        
        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        
        payload = {
            "message": content,
            "access_token": FACEBOOK_ACCESS_TOKEN
        }
        
        print("[INFO] Posting to Facebook...")
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            post_data = response.json()
            post_id = post_data.get('id')
            print()
            print("=" * 60)
            print("[SUCCESS] Successfully posted to Facebook!")
            print("=" * 60)
            print(f"Post ID: {post_id}")
            return True
        else:
            print(f"[ERROR] Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False


def main():
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*Facebook_Post_*.md'))
        
        if not posts:
            print("[ERROR] No Facebook posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"[INFO] Using: {filepath.name}\n")
    
    content = extract_content(filepath)
    post_to_facebook_api(content)


if __name__ == "__main__":
    main()