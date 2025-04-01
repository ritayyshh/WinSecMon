import subprocess
import logging

def get_system_info():
    logging.info("Fetching system information...")
    try:
        result = subprocess.run(["systeminfo"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to fetch system info: {e}")