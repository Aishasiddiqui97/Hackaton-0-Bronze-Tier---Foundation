#!/usr/bin/env python3
"""
Post to LinkedIn NOW - Immediate posting
"""

import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import random

try:
    from linkedin_auto_poster import LinkedInPoster
    LINKEDIN_AVAILABLE = True
except:
    LINKEDIN_AVAILABLE = False
    print("❌ LinkedIn poster not available")
    exit(1)

load_dotenv()


def generate_and_post_now():
    """Generate a post and post it immediately"""
    
    print("=" * 60)
    print("🚀 LinkedIn Instant Poster")
    print("=" * 60)
    print()
    
    # Post templates
    templates = [
        "🚀 Testing my new autonomous posting system! Excited about automation. #AI #Automation",
        "💡 Building cool stuff with Python and automation. #Python #Tech",
        "🤖 The future is automated! #Automation #Innovation",
        "🌟 Just shipped a new feature! #Development #Coding",
        "⚡ Speed and quality - that's the goal! #Engineering #Tech"
    ]
    
    # Select random content
    content = random.choice(templates)
    
    print(f"📝 Post content:\n{content}\n")
    print("-" * 60)
    
    # Create temporary file
    posted_folder = Path('03_Posted/History')
    posted_folder.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"LinkedIn_Post_{timestamp}.md"
    filepath = posted_folder / filename
    
    post_content = f"""---
platform: LinkedIn
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
status: instant-post
---

## Content

{content}

---
*Posted instantly via automation*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    print(f"✅ Post file created: {filename}\n")
    
    # Post to LinkedIn
    poster = None
    try:
        print("🌐 Initializing LinkedIn poster...")
        poster = LinkedInPoster(headless=False)
        poster.setup_driver()
        
        print("🔐 Logging in...")
        if not poster.login():
            print("❌ Login failed!")
            return False
        
        print("📤 Posting to LinkedIn...")
        if poster.post_from_file(str(filepath)):
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Post published to LinkedIn!")
            print("=" * 60)
            
            # Rename file
            new_name = f"POSTED_{filename}"
            new_path = filepath.parent / new_name
            filepath.rename(new_path)
            print(f"✅ File renamed to: {new_name}")
            
            return True
        else:
            print("\n❌ Failed to post")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
        
    finally:
        if poster:
            print("\n⏳ Waiting 5 seconds...")
            time.sleep(5)
            poster.close()


if __name__ == "__main__":
    generate_and_post_now()
    input("\nPress Enter to exit...")
