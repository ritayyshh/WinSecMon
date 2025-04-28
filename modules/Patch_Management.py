import subprocess
import logging

def check_patch_status():
    logging.info("Checking installed patches...")
    try:
        result = subprocess.run(["wmic", "qfe", "get", "HotFixID"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to check patch status: {e}")