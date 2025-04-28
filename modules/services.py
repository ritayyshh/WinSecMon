import subprocess
import logging

def audit_services():
    logging.info("Auditing running services...")
    try:
        result = subprocess.run(["wmic", "service", "get", "Name,State"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to audit services: {e}")

