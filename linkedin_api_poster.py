"""
LinkedIn API Poster - Official API Integration
Uses LinkedIn API v2 for autonomous posting
"""
import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class LinkedInAPIPoster:
    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_API_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("❌ LINKEDIN_API_ACCESS_TOKEN not found in .env file")
        
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Get user profile URN
        self.user_urn = self.get_user_profile()
    
    def get_user_profile(self):
        """Get LinkedIn user profile to get URN"""
        url = 'https://api.linkedin.com/v2/userinfo'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Extract user ID
            user_id = data.get('sub')
            if user_id:
                print(f"✅ LinkedIn Profile Connected: {data.get('name', 'Unknown')}")
                return f"urn:li:person:{user_id}"
            else:
                print("⚠️ Could not extract user ID from profile")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting profile: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def create_post(self, text):
        """Create a LinkedIn post using API v2"""
        if not self.user_urn:
            print("❌ User URN not available. Cannot post.")
            return False
        
        url = 'https://api.linkedin.com/v2/ugcPosts'
        
        post_data = {
            "author": self.user_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            print(f"📤 Posting to LinkedIn...")
            response = requests.post(url, headers=self.headers, json=post_data)
            response.raise_for_status()
            
            post_id = response.headers.get('X-RestLi-Id', 'Unknown')
            print(f"✅ Posted successfully! Post ID: {post_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error posting: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
    
    def post_from_file(self, filepath):
        """Read content from markdown file and post"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract content (remove metadata)
            lines = content.split('\n')
            text_lines = []
            in_metadata = False
            
            for line in lines:
                if line.strip().startswith('---'):
                    in_metadata = not in_metadata
                    continue
                if not in_metadata and line.strip() and not line.startswith('#'):
                    text_lines.append(line.strip())
            
            post_text = '\n\n'.join(text_lines)
            
            if not post_text:
                print(f"⚠️ No content found in {filepath}")
                return False
            
            print(f"\n📝 Content to post:\n{post_text}\n")
            return self.create_post(post_text)
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False


def test_linkedin_api():
    """Test LinkedIn API posting"""
    print("=" * 60)
    print("🚀 LinkedIn API Poster - Test Mode")
    print("=" * 60)
    
    try:
        poster = LinkedInAPIPoster()
        
        # Test with a simple post
        test_text = "🚀 Testing LinkedIn API integration! This post was created using the official LinkedIn API. #Automation #AI"
        
        print("\n📝 Test Post Content:")
        print(test_text)
        print("\n" + "=" * 60)
        
        success = poster.create_post(test_text)
        
        if success:
            print("\n✅ Test completed successfully!")
            print("Check your LinkedIn profile to see the post.")
        else:
            print("\n❌ Test failed. Check the error messages above.")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def post_pending_approvals():
    """Post all approved LinkedIn posts from 03_Posted/History folder"""
    print("=" * 60)
    print("🚀 LinkedIn API Autonomous Poster")
    print("=" * 60)
    
    try:
        poster = LinkedInAPIPoster()
        
        # Check for approved posts
        posted_folder = Path('03_Posted/History')
        if not posted_folder.exists():
            print("❌ 03_Posted/History folder not found")
            return
        
        # Find LinkedIn posts that haven't been posted yet
        linkedin_files = list(posted_folder.glob('LinkedIn_*.md'))
        posted_files = list(posted_folder.glob('POSTED_LinkedIn_*.md'))
        
        # Filter out already posted files
        pending_files = [f for f in linkedin_files if not f.name.startswith('POSTED_')]
        
        if not pending_files:
            print("✅ No pending LinkedIn posts found")
            return
        
        print(f"\n📋 Found {len(pending_files)} pending post(s)")
        
        for filepath in pending_files:
            print(f"\n{'=' * 60}")
            print(f"📄 Processing: {filepath.name}")
            
            success = poster.post_from_file(filepath)
            
            if success:
                # Rename file to mark as posted
                new_name = f"POSTED_{filepath.name}"
                new_path = filepath.parent / new_name
                filepath.rename(new_path)
                print(f"✅ Renamed to: {new_name}")
            else:
                print(f"❌ Failed to post: {filepath.name}")
            
            # Wait between posts
            time.sleep(5)
        
        print("\n" + "=" * 60)
        print("✅ Posting session complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test_linkedin_api()
        elif sys.argv[1] == 'post':
            post_pending_approvals()
        else:
            print("Usage:")
            print("  python linkedin_api_poster.py test   - Test API connection")
            print("  python linkedin_api_poster.py post   - Post approved content")
    else:
        # Default: post approved content
        post_pending_approvals()
