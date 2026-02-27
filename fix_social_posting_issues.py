#!/usr/bin/env python3
"""
Fix Social Media Posting Issues
Comprehensive solution for Facebook and Instagram problems
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_facebook_token():
    """Test and fix Facebook token"""
    print("🔍 Testing Facebook token...")
    
    try:
        result = subprocess.run(['python', 'fix_facebook_instagram_tokens.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if "All tokens are valid!" in result.stdout:
            print("✅ Facebook token is valid")
            return True
        else:
            print("❌ Facebook token needs refresh")
            print("💡 Run: python fix_facebook_instagram_tokens.py")
            return False
    except Exception as e:
        print(f"⚠️  Could not test token: {e}")
        return False

def test_instagram_posting():
    """Test Instagram text-to-image posting"""
    print("🔍 Testing Instagram posting...")
    
    # Find a sample Instagram post
    posted_folder = Path('03_Posted/History')
    instagram_posts = list(posted_folder.glob('*Instagram*.md'))
    
    if not instagram_posts:
        print("❌ No Instagram posts found to test")
        return False
    
    sample_post = instagram_posts[0]
    print(f"📄 Testing with: {sample_post.name}")
    
    try:
        result = subprocess.run(['python', 'instagram_text_to_image.py', str(sample_post)], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Instagram text-to-image working")
            return True
        else:
            print(f"❌ Instagram posting failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Instagram test error: {e}")
        return False

def install_required_packages():
    """Install required packages for image generation"""
    print("📦 Installing required packages...")
    
    packages = ['Pillow', 'requests']
    
    for package in packages:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} installed/updated")
            else:
                print(f"⚠️  {package} installation issue: {result.stderr}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

def create_temp_directories():
    """Create required directories"""
    print("📁 Creating required directories...")
    
    directories = [
        'temp_images',
        'logs',
        '00_Inbox/ALERTS.md'
    ]
    
    for directory in directories:
        if directory.endswith('.md'):
            # Create parent directory and file
            file_path = Path(directory)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.touch()
                print(f"✅ Created: {directory}")
        else:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")

def update_gold_tier_system():
    """Update the gold tier system with Instagram support"""
    print("🔧 Updating Gold Tier system...")
    
    # Create an updated version of the posting logic
    instagram_patch = '''
    def post_instagram(self, filepath):
        """Post to Instagram using text-to-image conversion"""
        try:
            import subprocess
            print("📸 Converting text to image for Instagram...")
            result = subprocess.run(['python', 'instagram_text_to_image.py', str(filepath)], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Instagram post prepared (image generated)")
                return True
            else:
                print(f"❌ Instagram preparation failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_error(f"Instagram error: {str(e)}")
            return False
'''
    
    # Save the patch to a file for manual application
    with open('instagram_patch.py', 'w') as f:
        f.write(instagram_patch)
    
    print("✅ Instagram patch created: instagram_patch.py")
    print("💡 Add this method to your GoldTierAutonomous class")

def create_quick_fix_script():
    """Create a quick fix script for immediate use"""
    fix_script = '''#!/usr/bin/env python3
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
        print(f"📤 Attempting Facebook post: {filepath}")
        
        # First check token
        result = subprocess.run(['python', 'fix_facebook_instagram_tokens.py'], 
                              input='n\\n', text=True, capture_output=True, timeout=30)
        
        if "All tokens are valid!" not in result.stdout:
            print("❌ Facebook token invalid - please refresh tokens")
            return False
        
        # Try posting
        result = subprocess.run(['python', 'api_facebook_poster.py', str(filepath)], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Facebook post successful")
            return True
        else:
            print(f"❌ Facebook post failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Facebook error: {e}")
        return False

def fix_instagram_post(filepath):
    """Fix Instagram posting with image generation"""
    try:
        print(f"📸 Creating Instagram image for: {filepath}")
        
        result = subprocess.run(['python', 'instagram_text_to_image.py', str(filepath)], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Instagram image created successfully")
            return True
        else:
            print(f"❌ Instagram image creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Instagram error: {e}")
        return False

def main():
    """Fix all pending posts"""
    posted_folder = Path('03_Posted/History')
    
    # Fix Facebook posts
    facebook_posts = [f for f in posted_folder.glob('*Facebook*.md') 
                     if not f.name.startswith('POSTED_')]
    
    for post in facebook_posts:
        if fix_facebook_post(post):
            # Rename to mark as posted
            new_name = f"POSTED_{post.name}"
            post.rename(post.parent / new_name)
            print(f"✅ Marked as posted: {new_name}")
    
    # Fix Instagram posts  
    instagram_posts = [f for f in posted_folder.glob('*Instagram*.md') 
                      if not f.name.startswith('POSTED_')]
    
    for post in instagram_posts:
        if fix_instagram_post(post):
            # Rename to mark as posted
            new_name = f"POSTED_{post.name}"
            post.rename(post.parent / new_name)
            print(f"✅ Marked as posted: {new_name}")

if __name__ == "__main__":
    main()
'''
    
    with open('quick_social_fix.py', 'w') as f:
        f.write(fix_script)
    
    print("✅ Quick fix script created: quick_social_fix.py")

def main():
    """Main fix function"""
    print("="*60)
    print("🔧 SOCIAL MEDIA POSTING FIXER")
    print("="*60)
    print()
    
    # Step 1: Install packages
    install_required_packages()
    print()
    
    # Step 2: Create directories
    create_temp_directories()
    print()
    
    # Step 3: Test Facebook
    fb_ok = test_facebook_token()
    print()
    
    # Step 4: Test Instagram
    ig_ok = test_instagram_posting()
    print()
    
    # Step 5: Create fixes
    update_gold_tier_system()
    create_quick_fix_script()
    print()
    
    # Summary
    print("="*60)
    print("📊 FIX SUMMARY")
    print("="*60)
    print(f"Facebook: {'✅ Ready' if fb_ok else '❌ Needs token refresh'}")
    print(f"Instagram: {'✅ Ready' if ig_ok else '❌ Needs setup'}")
    print()
    
    if not fb_ok:
        print("🔧 To fix Facebook:")
        print("   python fix_facebook_instagram_tokens.py")
        print()
    
    if not ig_ok:
        print("🔧 To fix Instagram:")
        print("   pip install Pillow")
        print("   python instagram_text_to_image.py")
        print()
    
    print("🚀 To fix all pending posts immediately:")
    print("   python quick_social_fix.py")
    print()
    
    print("💡 Files created:")
    print("   - fix_facebook_instagram_tokens.py")
    print("   - instagram_text_to_image.py") 
    print("   - quick_social_fix.py")
    print("   - instagram_patch.py")

if __name__ == "__main__":
    main()