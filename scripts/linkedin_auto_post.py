import os
import time
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_ROOT = Path("AI_Employee_Vault")
DONE_PATH = VAULT_ROOT / "Done"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
PLANS_PATH = VAULT_ROOT / "Plans"
LOG_PATH = "logs/actions.log"
DRAFT_FILE = NEEDS_ACTION_PATH / "linkedin_post_draft.md"

def log_event(event):
    """Log event with standardized timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_event = f"[{timestamp}] {event}"
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{formatted_event}\n")
        print(formatted_event)
    except Exception as e:
        print(f"[{timestamp}] ERROR - Failed to log: {e}")

def analyze_recent_activity():
    """Look at files in Done/ to find context for a post."""
    recent_files = sorted(list(DONE_PATH.glob("*.md")), key=os.path.getmtime, reverse=True)[:5]
    context = ""
    for f in recent_files:
        try:
            context += f.read_text(encoding='utf-8')[:100] + "\n"
        except Exception:
            continue
    return context if context else "Generic business growth and automation."

def generate_sales_post():
    """Generate a LinkedIn post draft following specific structure."""
    context = analyze_recent_activity()
    
    post_draft = f"""# LinkedIn Post Draft

Hook: Stop wasting time on manual outreach.
Problem: Most sales teams are drowned in emails and LinkedIn requests.
Solution: Our Digital FTE handles the sensors and reasoning for you.
CTA: DM me to learn how to scale your sales team with AI.

Hashtags: #AI #SalesAutomation #DigitalFTE #Productivity
"""
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Create the associated Plan.md for approval
    plan_content = f"""# Plan: Post to LinkedIn

Goal: Generate business sales post and publish.
Context: Based on recent activity: {context[:200]}...
Steps:
1. Generate draft
2. Wait for human approval (Approval Status: Pending)
3. Post via LinkedIn MCP

Risk Level: High
Approval Status: Pending
"""
    plan_file = PLANS_PATH / f"{timestamp}-PostPlan.md"
    
    try:
        NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)
        PLANS_PATH.mkdir(parents=True, exist_ok=True)

        with open(DRAFT_FILE, 'w', encoding='utf-8') as f:
            f.write(post_draft)
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
            
        log_event(f"LINKEDIN_POST_DRAFT_CREATED - {DRAFT_FILE.name}")
        log_event(f"LINKEDIN_PLAN_CREATED - {plan_file.name}")
        return DRAFT_FILE, plan_file
    except Exception as e:
        log_event(f"LINKEDIN_ERROR - Failed to generate post: {e}")
        return None, None

if __name__ == "__main__":
    generate_sales_post()
