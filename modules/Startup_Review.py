import subprocess
import logging

def check_startup_apps():
    logging.info("Checking startup applications...")
    try:
        result = subprocess.run(["wmic", "startup", "get", "Caption,Command"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to check startup applications: {e}")

