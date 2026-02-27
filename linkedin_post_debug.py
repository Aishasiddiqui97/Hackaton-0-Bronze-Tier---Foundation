#!/usr/bin/env python3
"""
LinkedIn Debug Mode - Browser stays open for manual inspection
"""

import sys
from pathlib import Path
from linkedin_auto_poster import LinkedInPoster

def debug_post(filepath):
    """Post with debug mode - browser stays open"""
    poster = None
    
    try:
        print("=" * 60)
        print("LinkedIn Debug Mode")
        print("=" * 60)
        print()
        print("⚠️  Browser will stay open for debugging")
        print("⚠️  Close manually when done")
        print()
        
        # Initialize poster (not headless)
        poster = LinkedInPoster(headless=False)
        poster.setup_driver()
        
        # Login
        print("🔐 Logging in...")
        if not poster.login():
            print("❌ Login failed")
            input("Press Enter to close browser...")
            return False
        
        print("✅ Login successful!")
        print()
        
        # Read content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract content
        lines = content.split('\n')
        post_content = []
        in_content_section = False
        
        for line in lines:
            if line.strip() == '## Content':
                in_content_section = True
                continue
            elif line.strip().startswith('##') and in_content_section:
                break
            elif in_content_section and line.strip():
                post_content.append(line.strip())
        
        final_content = '\n\n'.join(post_content)
        
        print(f"📄 Content to post:")
        print("-" * 60)
        print(final_content)
        print("-" * 60)
        print()
        
        input("Press Enter to start posting process...")
        
        # Try to post
        print("📝 Attempting to create post...")
        
        # Go to feed
        poster.driver.get('https://www.linkedin.com/feed/')
        print("✅ Navigated to feed")
        
        input("Press Enter to continue (check if feed loaded)...")
        
        # Take screenshot
        poster.driver.save_screenshot('debug_feed.png')
        print("📸 Screenshot saved: debug_feed.png")
        
        # Try to find start post button
        print("\n🔍 Looking for 'Start a post' button...")
        print("Check the browser - can you see the button?")
        
        input("Press Enter when ready to click 'Start a post'...")
        
        # Manual posting
        print("\n📝 Please complete the post manually in the browser")
        print("1. Click 'Start a post'")
        print("2. Paste this content:")
        print("-" * 60)
        print(final_content)
        print("-" * 60)
        print("3. Click 'Post' button")
        print()
        
        input("Press Enter when post is complete...")
        
        print("✅ Debug session complete!")
        print()
        
        keep_open = input("Keep browser open? (y/n): ")
        if keep_open.lower() != 'y':
            poster.close()
        else:
            print("Browser left open for inspection")
            print("Close manually when done")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if poster:
            poster.driver.save_screenshot('debug_error.png')
            print("📸 Error screenshot saved: debug_error.png")
        input("Press Enter to close...")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Find latest post
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        
        if not posts:
            print("❌ No LinkedIn posts found")
            sys.exit(1)
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}")
    
    debug_post(str(filepath))
