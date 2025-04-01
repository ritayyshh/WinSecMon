import logging
import os

LOG_FILE = "audit.log"

def setup_logging():
    """Sets up logging with file overwrite mode."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w"  # Overwrites the log file each time the script runs
    )

def clear_logs():
    """Clears the audit.log file manually."""
    try:
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, "w").close()  # Truncate the file
            print("Audit log cleared.")
        else:
            print("No audit log found.")
    except Exception as e:
        print(f"Error clearing log file: {e}")