#!/usr/bin/env python3
"""
Twitter OAuth 1.0a Implementation
Fixes the "Unsupported Authentication" error
"""

import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    print("⚠️  Tweepy not installed. Run: pip install tweepy")

load_dotenv()

# Twitter OAuth 1.0a credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


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


def post_tweet_oauth(content):
    """Post tweet using OAuth 1.0a (correct method)"""
    
    if not TWEEPY_AVAILABLE:
        print("❌ Tweepy not installed")
        print("💡 Run: pip install tweepy")
        return False
    
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("❌ Twitter OAuth credentials not found in .env")
        return False
    
    try:
        print("=" * 60)
        print("Twitter OAuth 1.0a Poster")
        print("=" * 60)
        print()
        print(f"📄 Content ({len(content)} chars):")
        print("-" * 60)
        print(content)
        print("-" * 60)
        print()
        
        # Authenticate using OAuth 1.0a
        auth = tweepy.OAuth1UserHandler(
            API_KEY, API_SECRET,
            ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
        
        # Create API object
        api = tweepy.API(auth)
        
        # Verify credentials
        print("🔐 Verifying credentials...")
        user = api.verify_credentials()
        print(f"✅ Authenticated as: @{user.screen_name}")
        print()
        
        # Post tweet
        print("📤 Posting tweet...")
        tweet = api.update_status(content)
        
        print()
        print("=" * 60)
        print("✅ Successfully posted to Twitter!")
        print("=" * 60)
        print(f"Tweet ID: {tweet.id}")
        print(f"URL: https://twitter.com/{user.screen_name}/status/{tweet.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
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
    post_tweet_oauth(content)


if __name__ == "__main__":
    main()
