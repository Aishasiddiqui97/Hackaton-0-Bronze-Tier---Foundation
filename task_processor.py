import os
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


# Path Configuration
VAULT_ROOT = Path(__file__).parent
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
DONE_PATH = VAULT_ROOT / "Done"
LOGS_PATH = VAULT_ROOT / "Logs"
SYSTEM_LOG_PATH = LOGS_PATH / "System_Log.md"
LOG_FILE = LOGS_PATH / "system.log"


def setup_logging():
    """Configure structured logging with rotation."""
    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('TaskProcessor')
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if function called multiple times
    if logger.handlers:
        return logger

    # Rotating file handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def read_task(task_file, logger):
    """Task Reader Skill: Read and parse task file."""
    try:
        logger.info(f"Reading task file: {task_file.name}")

        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.strip().split('\n')
        objective = lines[0] if lines else "No objective specified"

        task_data = {
            'file': task_file,
            'objective': objective,
            'content': content,
            'steps': [line.strip() for line in lines[1:] if line.strip()]
        }

        logger.info(f"Task parsed successfully: {task_file.name}")
        logger.info(f"Objective: {objective[:100]}...")  # Log first 100 chars

        return task_data

    except FileNotFoundError:
        logger.error(f"Task file not found: {task_file.name}")
        return None
    except PermissionError:
        logger.error(f"Permission denied reading task: {task_file.name}")
        return None
    except Exception as e:
        logger.error(f"Failed to read task {task_file.name}: {e}")
        return None


def process_task(task_data, logger):
    """Task Processor Skill: Execute task logic."""
    if not task_data:
        logger.warning("Attempted to process null task data")
        return False

    try:
        logger.info(f"Processing task: {task_data['file'].name}")
        logger.info(f"Task objective: {task_data['objective'][:100]}")

        if task_data['steps']:
            logger.info(f"Identified {len(task_data['steps'])} action items")
        else:
            logger.info("No explicit action items found in task")

        # Task processing logic here (currently simulation)
        logger.info(f"Task processing completed: {task_data['file'].name}")
        return True

    except Exception as e:
        logger.error(f"Error processing task {task_data['file'].name}: {e}")
        return False


def close_task(task_data, logger):
    """Task Closer Skill: Mark complete and move to Done."""
    if not task_data:
        logger.warning("Attempted to close null task data")
        return False

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_name = task_data['file'].name

        logger.info(f"Closing task: {task_name}")

        # Append completion marker
        completion_note = f"\n\n---\n\nStatus: Completed  \nTimestamp: {timestamp}\n"
        updated_content = task_data['content'] + completion_note

        # Write updated content
        with open(task_data['file'], 'w', encoding='utf-8') as f:
            f.write(updated_content)

        logger.info(f"Completion marker added to: {task_name}")

        # Ensure Done directory exists
        DONE_PATH.mkdir(parents=True, exist_ok=True)

        # Move to Done folder
        destination = DONE_PATH / task_name

        # Handle destination conflict
        if destination.exists():
            timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = destination.stem
            suffix = destination.suffix
            destination = DONE_PATH / f"{stem}_{timestamp_suffix}{suffix}"
            logger.warning(f"Destination exists, using: {destination.name}")

        task_data['file'].rename(destination)
        logger.info(f"Moved task to Done: {task_name}")

        # Log to System_Log.md
        log_entry(task_name, timestamp, logger)

        logger.info(f"Task closed successfully: {task_name}")
        return True

    except PermissionError as e:
        logger.error(f"Permission denied closing task {task_data['file'].name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to close task {task_data['file'].name}: {e}")
        return False


def log_entry(task_name, timestamp, logger):
    """Append log entry to System_Log.md."""
    try:
        SYSTEM_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Create System_Log.md if it doesn't exist
        if not SYSTEM_LOG_PATH.exists():
            with open(SYSTEM_LOG_PATH, 'w', encoding='utf-8') as f:
                f.write("# 📜 System Log\n\n## Activity Log\n\n")
            logger.info("Created System_Log.md")

        # Append log entry
        log_line = f"- **{timestamp}** - Completed: `{task_name}`\n"

        with open(SYSTEM_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_line)

        logger.info(f"Logged completion to System_Log.md: {task_name}")

    except Exception as e:
        logger.error(f"Failed to write log entry to System_Log.md: {e}")


def scan_and_process(logger):
    """Scan Needs_Action folder and process all tasks."""
    try:
        NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)
        logger.info(f"Scanning directory: {NEEDS_ACTION_PATH}")

        task_files = list(NEEDS_ACTION_PATH.glob("*.md"))

        if not task_files:
            logger.info("No tasks found in Needs_Action/")
            return

        logger.info(f"Found {len(task_files)} task(s) to process")

        # Process each task
        processed_count = 0
        failed_count = 0

        for task_file in task_files:
            logger.info(f"Starting task: {task_file.name}")

            task_data = read_task(task_file, logger)

            if task_data:
                success = process_task(task_data, logger)

                if success:
                    if close_task(task_data, logger):
                        processed_count += 1
                    else:
                        failed_count += 1
                        logger.error(f"Failed to close task: {task_file.name}")
                else:
                    failed_count += 1
                    logger.error(f"Failed to process task: {task_file.name}")
            else:
                failed_count += 1
                logger.error(f"Failed to read task: {task_file.name}")

        # Summary
        logger.info(f"Processing complete: {processed_count} succeeded, {failed_count} failed")

    except Exception as e:
        logger.error(f"Error during scan and process: {e}")


def main():
    """Main entry point."""
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Task Processor - Production Mode")
    logger.info("=" * 60)

    try:
        scan_and_process(logger)
        logger.info("Task processor finished successfully")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error in task processor: {e}")
        logger.info("=" * 60)
        raise


if __name__ == "__main__":
    main()
