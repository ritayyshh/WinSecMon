import subprocess
import logging

def check_firewall_status():
    logging.info("Checking Windows Firewall status...")
    try:
        result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True)
        logging.info(result.stdout)
    except Exception as e:
        logging.error(f"Failed to check firewall status: {e}")