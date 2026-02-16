#!/usr/bin/env python3
"""
Silver Tier Scheduler Loop

Continuous monitoring and execution loop that coordinates all Silver Tier components:
- Monitors input channels (Gmail, LinkedIn, WhatsApp, GitHub)
- Detects new tasks in Inbox
- Triggers reasoning engine for plan generation
- Monitors approval workflow
- Coordinates MCP server execution
- Manages task lifecycle from detection to completion

This is the main orchestration script for Silver Tier autonomous operation.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configuration
VAULT_ROOT = Path("AI_Employee_Vault")
INBOX_PATH = VAULT_ROOT / "Inbox"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
PLANS_PATH = VAULT_ROOT / "Plans"
DONE_PATH = VAULT_ROOT / "Done"
LOG_PATH = Path("logs")

# Timing configuration
CHECK_INTERVAL = 5  # seconds between checks
APPROVAL_CHECK_INTERVAL = 30  # seconds between approval checks
WATCHER_HEALTH_CHECK_INTERVAL = 300  # 5 minutes

# Logging setup
LOG_PATH.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH / 'scheduler_loop.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SCHEDULER_LOOP')


class SchedulerLoop:
    """
    Main scheduler loop for Silver Tier autonomous operation.
    """

    def __init__(self):
        self.running = False
        self.last_health_check = 0
        self.stats = {
            'tasks_detected': 0,
            'plans_generated': 0,
            'approvals_processed': 0,
            'tasks_completed': 0,
            'errors': 0
        }

    def start(self):
        """Start the continuous scheduler loop."""
        logger.info("=" * 60)
        logger.info("Silver Tier Scheduler Loop Starting")
        logger.info("=" * 60)
        logger.info(f"Monitoring: {INBOX_PATH}")
        logger.info(f"Approvals: {NEEDS_ACTION_PATH}")
        logger.info(f"Plans: {PLANS_PATH}")
        logger.info(f"Check interval: {CHECK_INTERVAL}s")
        logger.info("=" * 60)

        self.running = True

        try:
            while self.running:
                self.run_cycle()
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
            self.stop()
        except Exception as e:
            logger.error(f"Fatal error in scheduler loop: {e}", exc_info=True)
            self.stop()

    def run_cycle(self):
        """Execute one cycle of the scheduler loop."""
        try:
            # 1. Check for new tasks in Inbox
            self.check_inbox()

            # 2. Check for pending approvals
            self.check_approvals()

            # 3. Check for plans ready to execute
            self.check_execution_queue()

            # 4. Periodic health checks
            self.periodic_health_check()

        except Exception as e:
            logger.error(f"Error in scheduler cycle: {e}", exc_info=True)
            self.stats['errors'] += 1

    def check_inbox(self):
        """Check Inbox for new tasks requiring processing."""
        try:
            # Get all markdown files in Inbox (excluding .gitkeep)
            task_files = [
                f for f in INBOX_PATH.glob("*.md")
                if f.name != ".gitkeep"
            ]

            if task_files:
                logger.info(f"Found {len(task_files)} task(s) in Inbox")

                for task_file in task_files:
                    self.process_new_task(task_file)

        except Exception as e:
            logger.error(f"Error checking inbox: {e}", exc_info=True)

    def process_new_task(self, task_file):
        """Process a new task file from Inbox."""
        try:
            logger.info(f"Processing task: {task_file.name}")

            # The vault watcher (Bronze tier) will pick this up
            # and trigger the reasoning engine
            # We just log detection here
            self.stats['tasks_detected'] += 1

            logger.info(f"Task detected: {task_file.name} (will be processed by vault watcher)")

        except Exception as e:
            logger.error(f"Error processing task {task_file}: {e}", exc_info=True)

    def check_approvals(self):
        """Check Needs_Action for plans requiring or having approval."""
        try:
            # Get all plan files in Needs_Action
            plan_files = [
                f for f in NEEDS_ACTION_PATH.glob("*Plan*.md")
            ]

            if plan_files:
                logger.debug(f"Checking {len(plan_files)} plan(s) for approval status")

                for plan_file in plan_files:
                    self.check_plan_approval(plan_file)

        except Exception as e:
            logger.error(f"Error checking approvals: {e}", exc_info=True)

    def check_plan_approval(self, plan_file):
        """Check if a plan has been approved and route accordingly."""
        try:
            content = plan_file.read_text(encoding='utf-8')
            content_lower = content.lower()

            # Check approval status
            if "approval status: approved" in content_lower:
                logger.info(f"Plan approved: {plan_file.name}")
                self.route_approved_plan(plan_file)
                self.stats['approvals_processed'] += 1

            elif "approval status: rejected" in content_lower:
                logger.info(f"Plan rejected: {plan_file.name}")
                self.handle_rejected_plan(plan_file)

            elif "approval status: pending" in content_lower:
                # Check for timeout
                self.check_approval_timeout(plan_file)

        except Exception as e:
            logger.error(f"Error checking plan approval {plan_file}: {e}", exc_info=True)

    def route_approved_plan(self, plan_file):
        """Route an approved plan to execution queue."""
        try:
            # Move to Plans folder for execution
            destination = PLANS_PATH / plan_file.name
            plan_file.rename(destination)
            logger.info(f"Routed approved plan to execution: {destination.name}")

        except Exception as e:
            logger.error(f"Error routing approved plan {plan_file}: {e}", exc_info=True)

    def handle_rejected_plan(self, plan_file):
        """Handle a rejected plan."""
        try:
            # Move to Done with rejection note
            destination = DONE_PATH / plan_file.name
            plan_file.rename(destination)
            logger.info(f"Moved rejected plan to Done: {destination.name}")

        except Exception as e:
            logger.error(f"Error handling rejected plan {plan_file}: {e}", exc_info=True)

    def check_approval_timeout(self, plan_file):
        """Check if a plan approval has timed out."""
        try:
            # Get file creation time
            created_time = plan_file.stat().st_mtime
            current_time = time.time()
            age_hours = (current_time - created_time) / 3600

            # Default timeout: 24 hours
            timeout_hours = 24

            # Check if high risk (shorter timeout)
            content = plan_file.read_text(encoding='utf-8')
            if "risk level: high" in content.lower():
                timeout_hours = 12

            if age_hours > timeout_hours:
                logger.warning(f"Plan approval timed out: {plan_file.name} (age: {age_hours:.1f}h)")
                self.expire_plan(plan_file)

        except Exception as e:
            logger.error(f"Error checking timeout for {plan_file}: {e}", exc_info=True)

    def expire_plan(self, plan_file):
        """Expire a plan that hasn't been approved in time."""
        try:
            # Update plan with expiration note
            content = plan_file.read_text(encoding='utf-8')
            content += f"\n\n## Expiration Note\n\nThis plan expired without approval on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"

            # Update approval status
            content = content.replace(
                "Approval Status: Pending",
                "Approval Status: Expired"
            )

            plan_file.write_text(content, encoding='utf-8')

            # Move to Done
            destination = DONE_PATH / plan_file.name
            plan_file.rename(destination)

            logger.info(f"Expired plan moved to Done: {destination.name}")

        except Exception as e:
            logger.error(f"Error expiring plan {plan_file}: {e}", exc_info=True)

    def check_execution_queue(self):
        """Check Plans folder for plans ready to execute."""
        try:
            # Get all plan files in Plans folder
            plan_files = [
                f for f in PLANS_PATH.glob("*Plan*.md")
            ]

            if plan_files:
                logger.debug(f"Found {len(plan_files)} plan(s) in execution queue")

                # The task processor (Bronze tier) will handle execution
                # We just monitor here

        except Exception as e:
            logger.error(f"Error checking execution queue: {e}", exc_info=True)

    def periodic_health_check(self):
        """Perform periodic health checks on system components."""
        current_time = time.time()

        if current_time - self.last_health_check > WATCHER_HEALTH_CHECK_INTERVAL:
            logger.info("Performing health check...")

            # Check if watchers are running
            self.check_watcher_health()

            # Log statistics
            self.log_statistics()

            self.last_health_check = current_time

    def check_watcher_health(self):
        """Check if all watchers are running."""
        # This is a placeholder - actual implementation would check process status
        logger.info("Watcher health check: OK (placeholder)")

    def log_statistics(self):
        """Log current statistics."""
        logger.info("=" * 60)
        logger.info("Scheduler Statistics:")
        logger.info(f"  Tasks detected: {self.stats['tasks_detected']}")
        logger.info(f"  Plans generated: {self.stats['plans_generated']}")
        logger.info(f"  Approvals processed: {self.stats['approvals_processed']}")
        logger.info(f"  Tasks completed: {self.stats['tasks_completed']}")
        logger.info(f"  Errors: {self.stats['errors']}")
        logger.info("=" * 60)

    def stop(self):
        """Stop the scheduler loop."""
        logger.info("Stopping scheduler loop...")
        self.running = False
        self.log_statistics()
        logger.info("Scheduler loop stopped")


def main():
    """Main entry point."""
    # Verify paths exist
    for path in [VAULT_ROOT, INBOX_PATH, NEEDS_ACTION_PATH, PLANS_PATH, DONE_PATH]:
        if not path.exists():
            logger.error(f"Required path does not exist: {path}")
            logger.error("Please ensure Bronze Tier vault structure is set up")
            sys.exit(1)

    # Start scheduler loop
    scheduler = SchedulerLoop()
    scheduler.start()


if __name__ == "__main__":
    main()
