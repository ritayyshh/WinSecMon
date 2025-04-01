import subprocess
import logging

def check_antivirus():
    logging.info("Checking installed antivirus...")
    try:
        result = subprocess.run(["wmic", "antivirusproduct", "get", "displayName"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to check antivirus: {e}")