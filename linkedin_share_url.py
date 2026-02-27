#!/usr/bin/env python3
"""
LinkedIn Share URL Method - Opens pre-filled share dialog
Most reliable method - uses LinkedIn's official share URL
"""

import urllib.parse
import webbrowser
from pathlib import Path


def create_linkedin_share_url(content):
    """Create LinkedIn share URL with pre-filled content"""
    
    # LinkedIn share URL format
    base_url = "https://www.linkedin.com/sharing/share-offsite/"
    
    # URL encode the content
    encoded_content = urllib.parse.quote(content)
    
    # Create full URL
    share_url = f"{base_url}?url=https://linkedin.com&text={encoded_content}"
    
    return share_url


def extract_content_from_file(filepath):
    """Extract post content from markdown file"""
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
        elif in_content and line.strip():
            clean_line = line.strip()
            if not clean_line.startswith('#'):
                post_lines.append(clean_line)
    
    return '\n\n'.join(post_lines)


def main():
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Find latest post
        posted_folder = Path('03_Posted/History')
        posts = list(posted_folder.glob('*LinkedIn_Post_*.md'))
        
        if not posts:
            print("❌ No LinkedIn posts found")
            return
        
        filepath = max(posts, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {filepath.name}")
    
    # Extract content
    content = extract_content_from_file(filepath)
    
    print()
    print("=" * 60)
    print("LinkedIn Share URL Method")
    print("=" * 60)
    print()
    print(f"📄 Content ({len(content)} chars):")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()
    
    # Create share URL
    share_url = create_linkedin_share_url(content)
    
    print("🌐 Opening LinkedIn share dialog...")
    print()
    print("📝 Steps:")
    print("1. Browser will open with LinkedIn")
    print("2. Login if needed")
    print("3. Content will be pre-filled")
    print("4. Click 'Post' button")
    print()
    
    # Open in browser
    webbrowser.open(share_url)
    
    print("✅ Browser opened!")
    print("Complete the post in the browser window")


if __name__ == "__main__":
    main()
