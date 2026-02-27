#!/usr/bin/env python3
"""
Test LinkedIn Unicode/Emoji Posting
Creates a test post with emojis and special characters
"""

import os
from pathlib import Path
from datetime import datetime

def create_unicode_test_post():
    """Create a test post with Unicode characters and emojis"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Test content with various Unicode challenges
    test_content = f"""# LinkedIn Unicode Test Post

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Platform**: LinkedIn
**Test**: Unicode/Emoji Safety

---

## Content

🚀 Unicode Test Post! 

This post tests various character encodings:

✅ Basic emojis: 😀 😎 🎉 💼 📈
✅ Business emojis: 💡 🎯 📊 🔥 ⚡
✅ Special characters: café, naïve, résumé, Zürich
✅ Quotes: "Smart quotes" and 'apostrophes'
✅ Dashes: en-dash – and em-dash —
✅ Symbols: © ® ™ € £ ¥

🌟 Key Features:
• ChromeDriver BMP compatibility ✓
• Windows terminal encoding fix ✓  
• JavaScript injection method ✓
• Multiple selector strategies ✓

#Automation #Unicode #Testing #LinkedIn

---

**Status**: TEST_POST
**Encoding**: UTF-8 Safe
**Method**: Selenium + JavaScript Injection
"""
    
    # Create test post file
    folder = Path('03_Posted/History')
    folder.mkdir(parents=True, exist_ok=True)
    
    filename = f"LinkedIn_UnicodeTest_{timestamp}.md"
    filepath = folder / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("=" * 60)
    print("🧪 Unicode Test Post Created")
    print("=" * 60)
    print()
    print(f"📄 File: {filename}")
    print(f"📁 Location: {filepath}")
    print()
    print("Test includes:")
    print("✅ Emojis (🚀 😀 💼)")
    print("✅ Special characters (café, naïve)")
    print("✅ Smart quotes ("quotes")")
    print("✅ Dashes (– —)")
    print("✅ Currency symbols (€ £ ¥)")
    print()
    print("Next steps:")
    print("1. Run: python linkedin_selenium_fixed.py")
    print("2. Or: .\\test_linkedin_safe.bat")
    print()
    
    return str(filepath)

if __name__ == "__main__":
    create_unicode_test_post()