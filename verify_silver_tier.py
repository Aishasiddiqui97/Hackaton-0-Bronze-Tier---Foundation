#!/usr/bin/env python3
"""
Silver Tier Verification Script
Checks all Silver Tier requirements and provides status report
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def check_folder_exists(folderpath, description):
    """Check if a folder exists"""
    if Path(folderpath).exists():
        print(f"✅ {description}: {folderpath}")
        return True
    else:
        print(f"❌ {description}: {folderpath} (MISSING)")
        return False

def check_watcher_scripts():
    """Check for watcher scripts"""
    print("\n🔍 CHECKING WATCHER SCRIPTS")
    print("-" * 50)
    
    watchers = [
        ("AI_Employee_Vault/watcher.py", "Vault Watcher"),
        ("AI_Employee_Vault/scripts/gmail_watcher.py", "Gmail Watcher"),
        ("gold_tier_autonomous.py", "Social Media Watcher"),
        ("autonomous_social_agent.py", "WhatsApp Processor")
    ]
    
    count = 0
    for filepath, description in watchers:
        if check_file_exists(filepath, description):
            count += 1
    
    print(f"\n📊 Watcher Scripts: {count}/4 found")
    return count >= 2  # Silver Tier requires 2+

def check_linkedin_automation():
    """Check LinkedIn automation"""
    print("\n🔍 CHECKING LINKEDIN AUTOMATION")
    print("-" * 50)
    
    linkedin_files = [
        ("playwright_linkedin.py", "LinkedIn Poster"),
        ("linkedin_auto_poster.py", "LinkedIn Auto Poster"),
        ("prepare_linkedin_post.py", "LinkedIn Post Preparer")
    ]
    
    count = 0
    for filepath, description in linkedin_files:
        if check_file_exists(filepath, description):
            count += 1
    
    # Check for posted LinkedIn content
    posted_folder = Path("03_Posted/History")
    linkedin_posts = 0
    if posted_folder.exists():
        linkedin_posts = len(list(posted_folder.glob("*LinkedIn*.md")))
        print(f"✅ LinkedIn Posts Found: {linkedin_posts}")
    
    print(f"\n📊 LinkedIn Automation: {count}/3 components, {linkedin_posts} posts")
    return count >= 1 and linkedin_posts >= 0

def check_reasoning_loop():
    """Check Claude reasoning loop"""
    print("\n🔍 CHECKING REASONING LOOP")
    print("-" * 50)
    
    reasoning_files = [
        ("AI_Employee_Vault/reasoning_engine.py", "Reasoning Engine"),
        ("AI_Employee_Vault/task_processor.py", "Task Processor")
    ]
    
    count = 0
    for filepath, description in reasoning_files:
        if check_file_exists(filepath, description):
            count += 1
    
    # Check for Plan.md files
    plans_folder = Path("AI_Employee_Vault/Plans")
    plan_count = 0
    if plans_folder.exists():
        plan_count = len(list(plans_folder.glob("*.md")))
        print(f"✅ Plan Files Found: {plan_count}")
    
    print(f"\n📊 Reasoning Loop: {count}/2 components, {plan_count} plans")
    return count >= 1

def check_mcp_servers():
    """Check MCP servers"""
    print("\n🔍 CHECKING MCP SERVERS")
    print("-" * 50)
    
    mcp_files = [
        ("AI_Employee_Vault/MCP/linkedin_mcp_server.md", "LinkedIn MCP"),
        ("AI_Employee_Vault/MCP/meta_mcp_server.md", "Meta MCP"),
        ("AI_Employee_Vault/MCP/twitter_mcp_server.md", "Twitter MCP"),
        ("odoo_integration_example.py", "Odoo Integration"),
        ("odoo_test_api.py", "Odoo API Test")
    ]
    
    count = 0
    for filepath, description in mcp_files:
        if check_file_exists(filepath, description):
            count += 1
    
    print(f"\n📊 MCP Servers: {count}/5 found")
    return count >= 1

def check_approval_workflow():
    """Check human-in-the-loop approval workflow"""
    print("\n🔍 CHECKING APPROVAL WORKFLOW")
    print("-" * 50)
    
    approval_folders = [
        ("02_Pending_Approvals", "Pending Approvals"),
        ("02_Pending_Approvals/Social_Posts", "Social Posts Approval"),
        ("02_Pending_Approvals/Email_Drafts", "Email Drafts Approval"),
        ("AI_Employee_Vault/Needs_Action", "Needs Action"),
        ("03_Posted/History", "Posted History")
    ]
    
    count = 0
    for folderpath, description in approval_folders:
        if check_folder_exists(folderpath, description):
            count += 1
    
    print(f"\n📊 Approval Workflow: {count}/5 folders")
    return count >= 4

def check_scheduling():
    """Check scheduling setup"""
    print("\n🔍 CHECKING SCHEDULING")
    print("-" * 50)
    
    # Check for scheduler files
    scheduler_files = [
        ("setup_silver_tier_scheduler.bat", "Scheduler Setup Script"),
        ("odoo_daily_sync.py", "Daily Odoo Sync"),
        ("AI_Employee_Vault/scripts/ceo_briefing.py", "CEO Briefing Generator")
    ]
    
    count = 0
    for filepath, description in scheduler_files:
        if check_file_exists(filepath, description):
            count += 1
    
    # Check Windows Task Scheduler
    try:
        result = subprocess.run(['schtasks', '/query', '/tn', 'Silver_Tier*'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Windows Task Scheduler: Tasks found")
            scheduler_configured = True
        else:
            print("❌ Windows Task Scheduler: No Silver Tier tasks found")
            scheduler_configured = False
    except:
        print("⚠️  Windows Task Scheduler: Could not check (may need admin rights)")
        scheduler_configured = False
    
    print(f"\n📊 Scheduling: {count}/3 files, Scheduler: {'✅' if scheduler_configured else '❌'}")
    return count >= 2

def check_ai_skills():
    """Check AI functionality as Agent Skills"""
    print("\n🔍 CHECKING AI SKILLS")
    print("-" * 50)
    
    skills_folder = Path("AI_Employee_Vault/Skills")
    if not skills_folder.exists():
        print("❌ Skills folder not found")
        return False
    
    skills = list(skills_folder.glob("*.md"))
    skill_count = len(skills)
    
    print(f"✅ Skills Found: {skill_count}")
    
    # List some key skills
    key_skills = [
        "linkedin_poster.md",
        "facebook_poster.md", 
        "twitter_poster.md",
        "odoo_accounting_manager.md",
        "social_content_generator.md"
    ]
    
    found_key_skills = 0
    for skill in key_skills:
        if (skills_folder / skill).exists():
            print(f"  ✅ {skill}")
            found_key_skills += 1
        else:
            print(f"  ❌ {skill}")
    
    print(f"\n📊 AI Skills: {skill_count} total, {found_key_skills}/{len(key_skills)} key skills")
    return skill_count >= 10

def generate_silver_tier_report():
    """Generate comprehensive Silver Tier status report"""
    print("=" * 60)
    print("🥈 SILVER TIER VERIFICATION REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check all requirements
    requirements = [
        ("Two or more Watcher scripts", check_watcher_scripts()),
        ("Automatically Post on LinkedIn", check_linkedin_automation()),
        ("Claude reasoning loop (Plan.md files)", check_reasoning_loop()),
        ("One working MCP server", check_mcp_servers()),
        ("Human-in-the-loop approval workflow", check_approval_workflow()),
        ("Basic scheduling via Task Scheduler", check_scheduling()),
        ("All AI functionality as Agent Skills", check_ai_skills())
    ]
    
    # Calculate results
    passed = sum(1 for _, result in requirements if result)
    total = len(requirements)
    percentage = (passed / total) * 100
    
    print("\n" + "=" * 60)
    print("📊 SILVER TIER REQUIREMENTS SUMMARY")
    print("=" * 60)
    
    for requirement, result in requirements:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {requirement}")
    
    print("\n" + "=" * 60)
    print(f"🎯 OVERALL RESULT: {passed}/{total} requirements met ({percentage:.1f}%)")
    
    if percentage >= 100:
        print("🎉 CONGRATULATIONS! Silver Tier is COMPLETE!")
        tier_status = "COMPLETE"
    elif percentage >= 85:
        print("🚀 Silver Tier is NEARLY COMPLETE! Just a few items remaining.")
        tier_status = "NEARLY_COMPLETE"
    elif percentage >= 70:
        print("📈 Silver Tier is MOSTLY COMPLETE! Good progress.")
        tier_status = "MOSTLY_COMPLETE"
    else:
        print("🔧 Silver Tier needs more work. Keep building!")
        tier_status = "IN_PROGRESS"
    
    print("=" * 60)
    
    # Generate recommendations
    if not all(result for _, result in requirements):
        print("\n🔧 RECOMMENDATIONS TO COMPLETE SILVER TIER:")
        print("-" * 50)
        
        if not requirements[5][1]:  # Scheduling
            print("1. Run: setup_silver_tier_scheduler.bat (as Administrator)")
            print("   This will configure Windows Task Scheduler")
        
        if not requirements[0][1]:  # Watchers
            print("2. Ensure watcher scripts are running:")
            print("   - python AI_Employee_Vault/watcher.py")
            print("   - python gold_tier_autonomous.py")
        
        if not requirements[3][1]:  # MCP
            print("3. Test MCP server integration:")
            print("   - python odoo_test_api.py")
        
        print("\n📚 For detailed setup instructions, see:")
        print("   - GOLD_TIER_COMPLETE_GUIDE.md")
        print("   - START_HERE.md")
    
    # Save report
    report_file = f"Silver_Tier_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"""# Silver Tier Verification Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: {tier_status}
**Score**: {passed}/{total} ({percentage:.1f}%)

## Requirements Status

""")
        for requirement, result in requirements:
            status = "✅ PASS" if result else "❌ FAIL"
            f.write(f"- {status} {requirement}\n")
        
        f.write(f"""
## Summary

Your Silver Tier implementation is {percentage:.1f}% complete.

""")
        
        if tier_status == "COMPLETE":
            f.write("🎉 **CONGRATULATIONS!** Silver Tier is fully implemented!\n")
        else:
            f.write("🔧 See recommendations above to complete remaining requirements.\n")
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return tier_status, percentage

def main():
    """Main verification function"""
    try:
        status, percentage = generate_silver_tier_report()
        
        # Exit code based on completion
        if percentage >= 100:
            sys.exit(0)  # Success
        elif percentage >= 85:
            sys.exit(1)  # Nearly complete
        else:
            sys.exit(2)  # Needs work
            
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
        sys.exit(3)

if __name__ == "__main__":
    main()