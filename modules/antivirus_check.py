import subprocess
import logging
from datetime import datetime
import os

def setup_logging():
    """Configure logging to file (audit.log) and console"""
    log_filename = 'audit.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='a'),  # 'a' mode = append
            logging.StreamHandler()
        ]
    )
    logging.info(f"Logging to {os.path.abspath(log_filename)}")


def run_command(command, success_message="Command executed successfully"):
    """Helper function to run commands with better error handling"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=True
        )
        logging.info(success_message)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        logging.debug(f"Command: {e.cmd}")
        logging.debug(f"Return code: {e.returncode}")
        logging.debug(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error executing command: {e}")
        return None

def get_product_type(byte):
    """Map product type byte to human-readable description"""
    types = {
        0x00: "Invalid",
        0x01: "Antivirus",
        0x02: "Firewall",
        0x04: "Antispyware",
        0x08: "Internet settings",
        0x10: "User Account Control (UAC)",
        0x20: "Service"
    }
    return types.get(byte, f"Unknown (0x{byte:02X})")

def get_product_status(byte):
    """Map product status byte to human-readable description"""
    statuses = {
        0x00: "Non-functional",
        0x10: "Not running",
        0x20: "Running but out of date",
        0x30: "Running",
        0x40: "Running and up to date"
    }
    return statuses.get(byte & 0xF0, f"Unknown (0x{byte:02X})")

def get_signature_status(byte):
    """Map signature status byte to human-readable description"""
    statuses = {
        0x00: "Up to date",
        0x10: "Out of date",
        0x20: "Partially out of date"
    }
    return statuses.get(byte & 0xF0, f"Unknown (0x{byte:02X})")

def get_antivirus_details():
    """Retrieve detailed antivirus information using alternative methods"""
    try:
        logging.info("\n=== Antivirus Product Audit ===")
        
        # Try PowerShell alternative if WMIC fails
        ps_command = (
            "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | "
            "Select-Object displayName, instanceGuid, pathToSignedProductExe, "
            "pathToSignedReportingExe, productState, timestamp | Format-List"
        )
        
        result = run_command(
            ["powershell", "-Command", ps_command],
            "Successfully retrieved antivirus information via PowerShell"
        )
        
        if result:
            parse_antivirus_output(result)
        else:
            logging.warning("Attempting legacy WMIC command as fallback...")
            legacy_result = run_command(
                'wmic /namespace:\\\\root\\SecurityCenter2 path AntivirusProduct get * /format:list',
                "Successfully retrieved antivirus information via legacy WMIC"
            )
            if legacy_result:
                parse_antivirus_output(legacy_result)
            
    except Exception as e:
        logging.error(f"Unexpected error in get_antivirus_details: {e}")

def parse_antivirus_output(output):
    """Parse and log the antivirus information"""
    if not output:
        logging.warning("No antivirus products found or output is empty")
        return
    
    # Normalize line endings and split into products
    products = [p.strip() for p in output.replace('\r', '').split('\n\n') if p.strip()]
    
    for i, product in enumerate(products, 1):
        logging.info(f"\nAntivirus Product #{i}:")
        lines = [line.strip() for line in product.split('\n') if line.strip()]
        for line in lines:
            logging.info(line)
            
        # Extract and interpret product state if available
        product_state = next((line.split('=')[1] for line in lines if 'productState' in line.lower()), None)
        if product_state:
            interpret_product_state(product_state)

def interpret_product_state(state_hex):
    """Interpret the hexadecimal product state value"""
    try:
        state = int(state_hex)
        byte1 = state & 0xFF
        byte2 = (state >> 8) & 0xFF
        byte3 = (state >> 16) & 0xFF
        
        logging.info("\nProduct State Interpretation:")
        logging.info(f"Raw state value: 0x{state:06X}")
        logging.info(f"Byte 1 (0x{byte1:02X}): Product type - {get_product_type(byte1)}")
        logging.info(f"Byte 2 (0x{byte2:02X}): Product status - {get_product_status(byte2)}")
        logging.info(f"Byte 3 (0x{byte3:02X}): Signature status - {get_signature_status(byte3)}")
        
    except ValueError:
        logging.warning(f"Could not interpret product state value: {state_hex}")

def get_security_center_info():
    """Get additional information from Windows Security Center using PowerShell"""
    try:
        logging.info("\n=== Windows Security Center Information ===")
        
        # Check Security Center service
        service_status = run_command(
            "sc query wscsvc",
            "Retrieved Security Center service status"
        )
        
        # Get security provider information via PowerShell
        ps_command = (
            "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | "
            "Select-Object displayName, productState | Format-List; "
            "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName FirewallProduct | "
            "Select-Object displayName, productState | Format-List; "
            "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiSpywareProduct | "
            "Select-Object displayName, productState | Format-List"
        )
        
        providers = run_command(
            ["powershell", "-Command", ps_command],
            "Retrieved security providers information"
        )
        
    except Exception as e:
        logging.error(f"Error in get_security_center_info: {e}")

def check_windows_defender():
    """Specifically check Windows Defender status using PowerShell"""
    try:
        logging.info("\n=== Windows Defender Specific Check ===")
        
        # Check Defender status
        defender_status = run_command(
            ["powershell", "-Command", 
             "Get-MpComputerStatus | Select-Object * | Format-List"],
            "Retrieved Windows Defender status"
        )
        
        # Check Defender preferences
        defender_prefs = run_command(
            ["powershell", "-Command", "Get-MpPreference | Select-Object * | Format-List"],
            "Retrieved Windows Defender preferences"
        )
        
    except Exception as e:
        logging.error(f"Error in check_windows_defender: {e}")

def check_antivirus():
    """Main function to check antivirus status and related security information"""
    try:
        setup_logging()
        logging.info("Starting comprehensive antivirus audit...")
        
        # Check if we're running as administrator
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            
        if not is_admin:
            logging.warning("Warning: Not running as administrator. Some information may not be available.")
        
        # Get security information
        get_antivirus_details()
        get_security_center_info()
        check_windows_defender()
        
        logging.info("\n=== Antivirus Audit Completed ===")
        return True
    except Exception as e:
        logging.error(f"Antivirus audit failed: {e}")
        return False

if __name__ == "__main__":
    check_antivirus()