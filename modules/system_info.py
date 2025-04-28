import subprocess
import logging
import shutil
import os

def get_system_info():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting system information audit...")

    # Check for psinfo or systeminfo for basic system info
    psinfo_path = shutil.which("psinfo")  # Check if psinfo is in PATH

    try:
        if psinfo_path:
            logging.info(f"Found PsInfo at {psinfo_path}. Fetching system information using PsInfo...")
            result = subprocess.run(["psinfo"], capture_output=True, text=True)
        else:
            logging.warning("PsInfo not found. Falling back to systeminfo...")
            result = subprocess.run(["systeminfo"], capture_output=True, text=True)

        if result.returncode == 0:
            logging.info("System Information Retrieved Successfully:\n")
            logging.info(result.stdout)
        else:
            logging.error(f"Failed to retrieve system info. Exit code: {result.returncode}")
            logging.error(result.stderr)

    except FileNotFoundError as fnf_error:
        logging.error(f"Command not found. Make sure 'systeminfo' or 'psinfo' is available. Error: {fnf_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching system info: {e}")

    # Now check for pending file moves
    try:
        pendmoves_path = shutil.which("pendmoves")  # Check if pendmoves is in PATH
        if pendmoves_path:
            logging.info(f"Found PendMoves at {pendmoves_path}. Checking for pending file moves on next reboot...")
            result = subprocess.run(["pendmoves"], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Pending file moves retrieved successfully:\n")
                logging.info(result.stdout)
            else:
                logging.error(f"Failed to retrieve pending moves. Exit code: {result.returncode}")
                logging.error(result.stderr)
        else:
            logging.warning("PendMoves not found. Unable to check for pending file moves.")

    except FileNotFoundError as fnf_error:
        logging.error(f"Command not found. Make sure 'pendmoves' is available. Error: {fnf_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while checking for pending file moves: {e}")

    # Check autoruns for suspicious startup programs
    try:
        autoruns_path = shutil.which("autoruns")  # Check if autoruns is in PATH
        if autoruns_path:
            logging.info(f"Found Autoruns at {autoruns_path}. Checking for startup processes...")
            result = subprocess.run([autoruns_path, "-c"], capture_output=True, text=True)  # Run autoruns with CSV output
            if result.returncode == 0:
                logging.info("Autoruns information retrieved successfully:\n")
                logging.info(result.stdout)
            else:
                logging.error(f"Failed to retrieve autoruns information. Exit code: {result.returncode}")
                logging.error(result.stderr)
        else:
            logging.warning("Autoruns not found. Unable to check for autorun programs.")

    except FileNotFoundError as fnf_error:
        logging.error(f"Command not found. Make sure 'autoruns' is available. Error: {fnf_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while checking autoruns: {e}")

if __name__ == "__main__":
    get_system_info()