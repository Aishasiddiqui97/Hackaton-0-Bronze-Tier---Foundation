#!/usr/bin/env python3
"""
Hello World Test - Verify all platform connectivity
"""

import os
from pathlib import Path
from datetime import datetime

def create_hello_world_posts():
    """Create Hello World test posts for all platforms"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    hello_world_content = """# Hello World - Gold Tier System Test

**Generated**: {timestamp}
**Platform**: {platform}

---

## Content

🚀 Hello World!

This is an automated test post from the Gold Tier Autonomous System.

✅ System is live and operational
✅ Auto-posting enabled
✅ Ralph Wiggum Loop active

#Automation #GoldTier #AI

---

**Status**: TEST_POST
**System**: Fully Autonomous
"""
    
    platforms = ['LinkedIn', 'Twitter', 'Facebook', 'Instagram']
    folder = Path('03_Posted/History')
    folder.mkdir(parents=True, exist_ok=True)
    
    for platform in platforms:
        content = hello_world_content.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            platform=platform
        )
        
        filename = f"{platform}_HelloWorld_{timestamp}.md"
        filepath = folder / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {filename}")
    
    print()
    print("=" * 60)
    print("Hello World posts created!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start Gold Tier System: .\\start_gold_tier_system.bat")
    print("2. System will auto-post these test posts")
    print("3. Check System_Live_Status.md for status")


if __name__ == "__main__":
    create_hello_world_posts()
