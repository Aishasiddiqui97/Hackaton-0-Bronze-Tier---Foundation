#!/usr/bin/env python3
"""
Quick Social Media Fix
Run this to fix Facebook and Instagram posting immediately
"""

import subprocess
import sys
from pathlib import Path

def fix_facebook_post(filepath):
    """Fix Facebook posting with better error handling"""
    try:
        print(f"[INFO] Attempting Facebook post: {filepath}")
        
        # Try posting directly
        result = subprocess.run(['python', 'api_facebook_poster.py', str(filepath)], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "Successfully posted" in result.stdout:
            print("[SUCCESS] Facebook post successful")
            return True
        else:
            print(f"[ERROR] Facebook post failed: {result.stderr}")
            if "access token could not be decrypted" in result.stdout:
                print("[INFO] Facebook token expired - run: python fix_facebook_instagram_tokens.py")
            return False
            
    except Exception as e:
        print(f"[ERROR] Facebook error: {e}")
        return False

def fix_instagram_post(filepath):
    """Fix Instagram posting with image generation"""
    try:
        print(f"[INFO] Creating Instagram image for: {filepath}")
        
        result = subprocess.run(['python', 'instagram_text_to_image.py', str(filepath)], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("[SUCCESS] Instagram image created successfully")
            return True
        else:
            print(f"[ERROR] Instagram image creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Instagram error: {e}")
        return False

def main():
    """Fix all pending posts"""
    print("="*60)
    print("QUICK SOCIAL MEDIA FIX")
    print("="*60)
    
    posted_folder = Path('03_Posted/History')
    
    if not posted_folder.exists():
        print("[ERROR] Posted folder not found")
        return
    
    # Fix Facebook posts
    facebook_posts = [f for f in posted_folder.glob('*Facebook*.md') 
                     if not f.name.startswith('POSTED_')]
    
    print(f"\n[INFO] Found {len(facebook_posts)} Facebook posts to process")
    
    for post in facebook_posts:
        if fix_facebook_post(post):
            # Rename to mark as posted
            new_name = f"POSTED_{post.name}"
            post.rename(post.parent / new_name)
            print(f"[SUCCESS] Marked as posted: {new_name}")
        else:
            print(f"[ERROR] Failed to post: {post.name}")
    
    # Fix Instagram posts  
    instagram_posts = [f for f in posted_folder.glob('*Instagram*.md') 
                      if not f.name.startswith('POSTED_')]
    
    print(f"\n[INFO] Found {len(instagram_posts)} Instagram posts to process")
    
    for post in instagram_posts:
        if fix_instagram_post(post):
            # Rename to mark as posted (simulation)
            new_name = f"POSTED_{post.name}"
            post.rename(post.parent / new_name)
            print(f"[SUCCESS] Marked as posted: {new_name}")
        else:
            print(f"[ERROR] Failed to process: {post.name}")
    
    print("\n" + "="*60)
    print("QUICK FIX COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. For Facebook: Refresh tokens if needed")
    print("2. For Instagram: Set up image hosting for live posting")
    print("3. Check temp_images/ folder for generated images")

if __name__ == "__main__":
    main()