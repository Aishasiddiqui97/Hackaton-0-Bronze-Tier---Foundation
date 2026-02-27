"""
Verify Gold Tier System - Complete Check
"""
import os
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking Gold Tier files...")
    
    required_files = [
        'README.md',
        'GOLD_TIER_STATUS.md',
        'SILVER_TIER_UPDATE.md',
        'requirements.txt',
        '.gitignore',
        'LICENSE',
        'linkedin_auto_poster.py',
        'fully_autonomous_linkedin.py',
        'post_now_linkedin.py',
        'test_linkedin_login.py',
        'docker-compose.yml',
        'odoo_integration_example.py',
        '.env.template',
        'push_to_github.bat',
        'post_now.bat',
        'start_fully_autonomous.bat',
        'test_login.bat'
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing.append(file)
    
    return len(missing) == 0

def check_folders():
    """Check if required folders exist"""
    print("\n🔍 Checking folder structure...")
    
    required_folders = [
        '00_Inbox',
        '01_Drafts/Auto_Generated',
        '02_Pending_Approvals/Social_Posts',
        '03_Posted/History',
        'AI_Employee_Vault',
        'config'
    ]
    
    missing = []
    for folder in required_folders:
        if Path(folder).exists():
            print(f"✅ {folder}")
        else:
            print(f"❌ {folder} - MISSING!")
            missing.append(folder)
    
    return len(missing) == 0

def check_env():
    """Check environment configuration"""
    print("\n🔍 Checking environment...")
    
    if Path('.env').exists():
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'LINKEDIN_EMAIL' in content:
                print("✅ LinkedIn credentials configured")
            else:
                print("⚠️ LinkedIn credentials not found")
    else:
        print("⚠️ .env file not found (use .env.template)")
    
    if Path('.env.template').exists():
        print("✅ .env.template exists")
    
    return True

def check_git():
    """Check Git configuration"""
    print("\n🔍 Checking Git...")
    
    if Path('.git').exists():
        print("✅ Git repository initialized")
    else:
        print("❌ Git repository not initialized")
        print("   Run: git init")
        return False
    
    if Path('.gitignore').exists():
        print("✅ .gitignore configured")
    
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("🏆 Gold Tier System Verification")
    print("=" * 60)
    print()
    
    checks = {
        'Files': check_files(),
        'Folders': check_folders(),
        'Environment': check_env(),
        'Git': check_git()
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
        print("🎉 Gold Tier system is ready!")
        print("\nNext steps:")
        print("1. Configure .env file with credentials")
        print("2. Test: .\\test_login.bat")
        print("3. Push: .\\push_to_github.bat")
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
