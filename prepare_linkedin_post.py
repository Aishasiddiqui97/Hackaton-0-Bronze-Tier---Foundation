#!/usr/bin/env python3
"""
LinkedIn Post Preparer - Extracts content and copies to clipboard
Then you just paste on LinkedIn (takes 5 seconds)
"""

import sys
from pathlib import Path
import pyperclip


def extract_content_from_file(filepath):
    """Extract clean post content"""
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
            if not clean_line.startswith('#') and clean_line != '---':
                post_lines.append(clean_line)
    
    return '\n\n'.join(post_lines)


def main():
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
    print("LinkedIn Post Ready!")
    print("=" * 60)
    print()
    print("📋 Content copied to clipboard!")
    print()
    print("📝 Next steps (takes 5 seconds):")
    print("1. Go to: https://www.linkedin.com")
    print("2. Click 'Start a post'")
    print("3. Press Ctrl+V to paste")
    print("4. Click 'Post' button")
    print()
    print("=" * 60)
    print("Content Preview:")
    print("=" * 60)
    print(content)
    print("=" * 60)
    print()
    
    # Copy to clipboard
    try:
        pyperclip.copy(content)
        print("✅ Content copied to clipboard!")
        print("✅ Ready to paste on LinkedIn!")
    except:
        print("⚠️  Clipboard copy failed. Install: pip install pyperclip")
        print("📄 Copy the content above manually")
    
    # Open LinkedIn
    import webbrowser
    print()
    print("🌐 Opening LinkedIn...")
    webbrowser.open('https://www.linkedin.com/feed/')
    
    print()
    print("✅ All set! Just paste and post!")


if __name__ == "__main__":
    main()
