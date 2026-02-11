import os
import sys
import time
import signal
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Path Configuration
VAULT_ROOT = Path(__file__).parent
INBOX_PATH = VAULT_ROOT / "Inbox"
NEEDS_ACTION_PATH = VAULT_ROOT / "Needs_Action"
LOGS_PATH = VAULT_ROOT / "Logs"
TASK_PROCESSOR_SCRIPT = VAULT_ROOT / "task_processor.py"
LOG_FILE = LOGS_PATH / "system.log"

# Temporary file patterns to ignore
TEMP_FILE_PATTERNS = ['.tmp', '~', '.swp', '.swo', '.bak']


def setup_logging():
    """Configure structured logging with rotation."""
    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('WatcherService')
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
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class InboxHandler(FileSystemEventHandler):
    """Production-ready file system event handler with duplicate protection."""

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.processed_files = {}  # {file_hash: timestamp}
        self.processing_lock = set()  # Files currently being processed

    def _is_temp_file(self, filename):
        """Check if file is a temporary file that should be ignored."""
        name_lower = filename.lower()
        return any(pattern in name_lower for pattern in TEMP_FILE_PATTERNS)

    def _get_file_hash(self, file_path):
        """Generate hash of file path and modification time for duplicate detection."""
        try:
            stat = file_path.stat()
            hash_input = f"{file_path.name}_{stat.st_size}_{stat.st_mtime}"
            return hashlib.md5(hash_input.encode()).hexdigest()
        except Exception as e:
            self.logger.warning(f"Failed to generate hash for {file_path.name}: {e}")
            return None

    def _is_duplicate(self, file_hash):
        """Check if file was recently processed (within last 60 seconds)."""
        if file_hash in self.processed_files:
            time_diff = time.time() - self.processed_files[file_hash]
            if time_diff < 60:
                return True
            else:
                # Clean up old entry
                del self.processed_files[file_hash]
        return False

    def _safe_move_file(self, source, destination):
        """Safely move file with conflict resolution."""
        try:
            # Check if source still exists
            if not source.exists():
                self.logger.warning(f"Source file disappeared: {source.name}")
                return False

            # Handle destination conflict
            if destination.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = destination.stem
                suffix = destination.suffix
                destination = destination.parent / f"{stem}_{timestamp}{suffix}"
                self.logger.warning(f"Destination exists, using: {destination.name}")

            # Perform move
            source.rename(destination)
            self.logger.info(f"Moved: {source.name} → Needs_Action/")
            return True

        except PermissionError as e:
            self.logger.error(f"Permission denied moving {source.name}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to move {source.name}: {e}")
            return False

    def _trigger_task_processor(self, filename):
        """Execute task processor script."""
        try:
            result = subprocess.run(
                [sys.executable, str(TASK_PROCESSOR_SCRIPT)],
                check=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            self.logger.info(f"Task processor executed for: {filename}")

            if result.stdout:
                self.logger.info(f"Processor output: {result.stdout.strip()}")

        except subprocess.TimeoutExpired:
            self.logger.error(f"Task processor timeout for: {filename}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Task processor failed for {filename}: {e.stderr}")
        except Exception as e:
            self.logger.error(f"Failed to run task processor for {filename}: {e}")

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Filter: only .md files
        if file_path.suffix.lower() != ".md":
            return

        # Filter: ignore temporary files
        if self._is_temp_file(file_path.name):
            self.logger.info(f"Ignored temporary file: {file_path.name}")
            return

        # Check if already processing this file
        if file_path.name in self.processing_lock:
            self.logger.warning(f"Already processing: {file_path.name}")
            return

        try:
            # Wait for file write to complete
            time.sleep(0.5)

            # Generate file hash for duplicate detection
            file_hash = self._get_file_hash(file_path)

            if file_hash and self._is_duplicate(file_hash):
                self.logger.warning(f"Duplicate detected, skipping: {file_path.name}")
                return

            # Mark as processing
            self.processing_lock.add(file_path.name)

            # Log detection
            self.logger.info(f"Detected new file: {file_path.name}")

            # Move file to Needs_Action
            destination = NEEDS_ACTION_PATH / file_path.name

            if self._safe_move_file(file_path, destination):
                # Mark as processed
                if file_hash:
                    self.processed_files[file_hash] = time.time()

                # Trigger task processor
                self._trigger_task_processor(file_path.name)

        except FileNotFoundError:
            self.logger.warning(f"File disappeared before processing: {file_path.name}")
        except Exception as e:
            self.logger.error(f"Unexpected error processing {file_path.name}: {e}")
        finally:
            # Release processing lock
            self.processing_lock.discard(file_path.name)

    def cleanup_old_entries(self):
        """Remove processed file entries older than 5 minutes."""
        current_time = time.time()
        to_remove = [
            hash_key for hash_key, timestamp in self.processed_files.items()
            if current_time - timestamp > 300
        ]
        for hash_key in to_remove:
            del self.processed_files[hash_key]


class WatcherService:
    """Production watcher service with graceful shutdown."""

    def __init__(self):
        self.logger = setup_logging()
        self.observer = None
        self.handler = None
        self.running = False

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        sig_name = signal.Signals(signum).name
        self.logger.info(f"Received {sig_name}, initiating graceful shutdown...")
        self.stop()

    def _validate_environment(self):
        """Validate required directories and files exist."""
        try:
            INBOX_PATH.mkdir(parents=True, exist_ok=True)
            NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)
            LOGS_PATH.mkdir(parents=True, exist_ok=True)

            if not TASK_PROCESSOR_SCRIPT.exists():
                self.logger.warning(f"task_processor.py not found at {TASK_PROCESSOR_SCRIPT}")
                self.logger.warning("Watcher will run but task processing will fail")

            self.logger.info("Environment validation complete")
            return True

        except Exception as e:
            self.logger.error(f"Environment validation failed: {e}")
            return False

    def start(self):
        """Start the watcher service."""
        try:
            self.logger.info("=" * 60)
            self.logger.info("Digital FTE Watcher Service - Production Mode")
            self.logger.info("=" * 60)

            # Validate environment
            if not self._validate_environment():
                self.logger.error("Cannot start service due to validation errors")
                return False

            # Initialize handler and observer
            self.handler = InboxHandler(self.logger)
            self.observer = Observer()
            self.observer.schedule(self.handler, str(INBOX_PATH), recursive=False)

            # Start observer
            self.observer.start()
            self.running = True

            self.logger.info(f"Monitoring: {INBOX_PATH}")
            self.logger.info("Service started successfully")
            self.logger.info("Press Ctrl+C to stop")

            # Main loop with periodic cleanup
            cleanup_counter = 0
            while self.running:
                time.sleep(1)
                cleanup_counter += 1

                # Cleanup old entries every 60 seconds
                if cleanup_counter >= 60:
                    self.handler.cleanup_old_entries()
                    cleanup_counter = 0

            return True

        except Exception as e:
            self.logger.error(f"Failed to start watcher service: {e}")
            return False

    def stop(self):
        """Stop the watcher service gracefully."""
        if not self.running:
            return

        self.running = False
        self.logger.info("Stopping watcher service...")

        try:
            if self.observer:
                self.observer.stop()
                self.observer.join(timeout=5)

            self.logger.info("Watcher service stopped successfully")
            self.logger.info("=" * 60)

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


def main():
    """Main entry point."""
    service = WatcherService()

    try:
        service.start()
    except Exception as e:
        if service.logger:
            service.logger.error(f"Fatal error: {e}")
        else:
            print(f"FATAL ERROR: {e}")
        sys.exit(1)
    finally:
        service.stop()


if __name__ == "__main__":
    main()
