#!/usr/bin/env python3
"""
Instagram API Poster - Uses Access Token
Posts to Instagram Business Account
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')


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
    
    # Instagram caption limit: 2200 chars
    full_content = '\n\n'.join(post_lines)
    if len(full_content) > 2200:
        full_content = full_content[:2197] + '...'
    
    return full_content


def post_to_instagram_api(content, image_url=None):
    """Post to Instagram using Graph API"""
    
    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("❌ Instagram credentials not found in .env")
        return False
    
    try:
        print("=" * 60)
        print("Instagram API Poster")
        print("=" * 60)
        print()
        print(f"📄 Caption ({len(content)} chars):")
        print("-" * 60)
        print(content)
        print("-" * 60)
        print()
        
        # Note: Instagram requires an image URL
        # For text-only posts, you'd need to generate an image
        if not image_url:
            print("⚠️  Instagram requires an image")
            print("💡 Text-only posting not supported by Instagram API")
            print("💡 Use Instagram app or generate image from text")
            return False
        
        # Instagram Graph API endpoint
        url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
        
        # Step 1: Create media container
        payload = {
            "image_url": image_url,
            "caption": content,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        
        print("📤 Creating Instagram media container...")
        response = requests.post(url, data=payload)
        
        if response.status_code != 200:
            print(f"❌ Error creating container: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        container_id = response.json().get('id')
        print(f"✅ Container created: {container_id}")
        
        # Step 2: Publish media
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        
        print("📤 Publishing to Instagram...")
        publish_response = requests.post(publish_url, data=publish_payload)
        
        if publish_response.status_code == 200:
            post_id = publish_response.json().get('id')
            print()
            print("=" * 60)
            print("✅ Successfully posted to Instagram!")
            print("=" * 60)
            print(f"Post ID: {post_id}")
            return True
        else:
            print(f"❌ Error publishing: {publish_response.status_code}")
            print(f"Response: {publish_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*Instagram_Post_*.md'))
        
        if not posts:
            print("❌ No Instagram posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    content = extract_content(filepath)
    
    # Instagram requires image - for now just show message
    print("⚠️  Instagram API requires an image URL")
    print("💡 For text-only posts, use Instagram app")
    print()
    print("Caption ready:")
    print(content)


if __name__ == "__main__":
    main()
