#!/usr/bin/env python3
"""
LinkedIn Manual Posting Helper
Browser khulega, aap manually post kar sakte ho
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

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

def manual_linkedin_helper():
    """Open LinkedIn and help with manual posting"""
    
    # Find latest LinkedIn post
    posted_folder = Path('03_Posted/History')
    posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
    
    if not posts:
        print("❌ No LinkedIn posts found in 03_Posted/History/")
        return
    
    # Get unposted files
    unposted = [p for p in posts if not p.name.startswith('POSTED_')]
    
    if not unposted:
        print("✅ All LinkedIn posts already posted!")
        return
    
    filepath = unposted[0]  # Get first unposted
    
    print("=" * 60)
    print("🔵 LinkedIn Manual Posting Helper")
    print("=" * 60)
    print()
    print(f"📄 File: {filepath.name}")
    print()
    
    # Extract and show content
    content = extract_content(str(filepath))
    
    print("📝 CONTENT TO POST:")
    print("-" * 40)
    print(content)
    print("-" * 40)
    print()
    
    # Copy to clipboard if possible
    try:
        import pyperclip
        pyperclip.copy(content)
        print("✅ Content copied to clipboard!")
        print()
    except:
        print("💡 Install pyperclip for auto-copy: pip install pyperclip")
        print()
    
    if PLAYWRIGHT_AVAILABLE:
        print("🌐 Opening LinkedIn in browser...")
        print()
        print("MANUAL STEPS:")
        print("1. Login to LinkedIn (if needed)")
        print("2. Click 'Start a post'")
        print("3. Paste the content (Ctrl+V)")
        print("4. Click 'Post'")
        print("5. Come back here and press Enter")
        print()
        
        # Open browser
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # Go to LinkedIn
            page.goto('https://www.linkedin.com/feed/')
            
            # Wait for user to post manually
            input("Press Enter after you've posted manually...")
            
            browser.close()
        
        # Mark as posted
        new_name = f"POSTED_{filepath.name}"
        new_path = filepath.parent / new_name
        filepath.rename(new_path)
        
        print(f"✅ Marked as posted: {new_name}")
        
    else:
        print("❌ Playwright not available")
        print("💡 Manual steps:")
        print("1. Go to https://www.linkedin.com/feed/")
        print("2. Login if needed")
        print("3. Click 'Start a post'")
        print("4. Copy-paste the content above")
        print("5. Click 'Post'")
        print()
        
        confirm = input("Did you post it manually? (y/n): ")
        if confirm.lower() == 'y':
            new_name = f"POSTED_{filepath.name}"
            new_path = filepath.parent / new_name
            filepath.rename(new_path)
            print(f"✅ Marked as posted: {new_name}")

def check_all_linkedin_posts():
    """Check all pending LinkedIn posts"""
    posted_folder = Path('03_Posted/History')
    posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
    
    unposted = [p for p in posts if not p.name.startswith('POSTED_')]
    
    print(f"📊 LinkedIn Posts Status:")
    print(f"   Total: {len(posts)}")
    print(f"   Posted: {len(posts) - len(unposted)}")
    print(f"   Pending: {len(unposted)}")
    print()
    
    if unposted:
        print("📋 Pending Posts:")
        for post in unposted:
            print(f"   - {post.name}")
        print()
        
        choice = input("Process next post? (y/n): ")
        if choice.lower() == 'y':
            manual_linkedin_helper()
    else:
        print("✅ All posts are already posted!")

if __name__ == "__main__":
    print("Choose option:")
    print("1. Process next LinkedIn post")
    print("2. Check all LinkedIn posts status")
    
    choice = input("Enter choice (1/2): ")
    
    if choice == '1':
        manual_linkedin_helper()
    elif choice == '2':
        check_all_linkedin_posts()
    else:
        print("Invalid choice")