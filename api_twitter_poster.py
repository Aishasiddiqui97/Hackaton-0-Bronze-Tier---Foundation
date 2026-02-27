#!/usr/bin/env python3
"""
Twitter API v2 Poster - Uses Bearer Token
More reliable than browser automation
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


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
    
    # Twitter 280 char limit
    full_content = '\n\n'.join(post_lines)
    if len(full_content) > 280:
        full_content = full_content[:277] + '...'
    
    return full_content


def post_tweet_api(content):
    """Post tweet using Twitter API v2"""
    
    if not TWITTER_BEARER_TOKEN:
        print("❌ Twitter Bearer Token not found in .env")
        return False
    
    try:
        print("=" * 60)
        print("Twitter API Poster")
        print("=" * 60)
        print()
        print(f"📄 Content ({len(content)} chars):")
        print("-" * 60)
        print(content)
        print("-" * 60)
        print()
        
        # Twitter API v2 endpoint
        url = "https://api.twitter.com/2/tweets"
        
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": content
        }
        
        print("📤 Posting to Twitter...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            tweet_data = response.json()
            tweet_id = tweet_data.get('data', {}).get('id')
            print()
            print("=" * 60)
            print("✅ Successfully posted to Twitter!")
            print("=" * 60)
            print(f"Tweet ID: {tweet_id}")
            print(f"URL: https://twitter.com/i/web/status/{tweet_id}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
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
        posts = list(posted_folder.glob('*Twitter_Post_*.md'))
        
        if not posts:
            print("❌ No Twitter posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}\n")
    
    content = extract_content(filepath)
    post_tweet_api(content)


if __name__ == "__main__":
    main()
