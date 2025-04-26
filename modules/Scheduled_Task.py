import subprocess
import logging

def check_scheduled_tasks():
    logging.info("Checking scheduled tasks...")
    try:
        result = subprocess.run(["schtasks"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to check scheduled tasks: {e}")

