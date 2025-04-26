import subprocess
import logging

def list_installed_apps():
    logging.info("Listing installed applications...")
    try:
        result = subprocess.run(["wmic", "product", "get", "Name"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to list installed applications: {e}")

