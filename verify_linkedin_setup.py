"""
Verify LinkedIn API Setup
Check if everything is configured correctly
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and has LinkedIn token"""
    print("🔍 Checking .env file...")
    
    if not Path('.env').exists():
        print("❌ .env file not found!")
        return False
    
    load_dotenv()
    token = os.getenv('LINKEDIN_API_ACCESS_TOKEN')
    
    if not token:
        print("❌ LINKEDIN_API_ACCESS_TOKEN not found in .env")
        return False
    
    if len(token) < 100:
        print("⚠️ LinkedIn token seems too short")
        return False
    
    print(f"✅ LinkedIn API token found ({len(token)} characters)")
    return True

def check_folders():
    """Check if required folders exist"""
    print("\n🔍 Checking folders...")
    
    folders = [
        '00_Inbox',
        '01_Drafts/Auto_Generated',
        '02_Pending_Approvals/Social_Posts',
        '03_Posted/History'
    ]
    
    all_exist = True
    for folder in folders:
        if Path(folder).exists():
            print(f"✅ {folder}")
        else:
            print(f"❌ {folder} - Missing!")
            all_exist = False
    
    return all_exist

def check_scripts():
    """Check if required scripts exist"""
    print("\n🔍 Checking scripts...")
    
    scripts = [
        'linkedin_api_poster.py',
        'gold_tier_autonomous_api.py',
        'test_linkedin_api.bat',
        'start_linkedin_api_poster.bat',
        'start_gold_tier_api.bat'
    ]
    
    all_exist = True
    for script in scripts:
        if Path(script).exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - Missing!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    packages = {
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'pathlib': 'pathlib (built-in)'
    }
    
    all_installed = True
    for module, package in packages.items():
        try:
            __import__(module.replace('dotenv', 'dotenv'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed!")
            print(f"   Install: pip install {package}")
            all_installed = False
    
    return all_installed

def test_linkedin_api():
    """Test LinkedIn API connection"""
    print("\n🔍 Testing LinkedIn API connection...")
    
    try:
        from linkedin_api_poster import LinkedInAPIPoster
        
        poster = LinkedInAPIPoster()
        
        if poster.user_urn:
            print("✅ LinkedIn API connection successful!")
            return True
        else:
            print("❌ LinkedIn API connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("🔍 LinkedIn API Setup Verification")
    print("=" * 60)
    print()
    
    checks = {
        'Environment File': check_env_file(),
        'Folder Structure': check_folders(),
        'Required Scripts': check_scripts(),
        'Dependencies': check_dependencies(),
        'LinkedIn API': test_linkedin_api()
    }
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    all_passed = all(checks.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Run: test_linkedin_api.bat")
        print("2. Run: start_gold_tier_api.bat")
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
