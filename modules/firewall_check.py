import subprocess
import logging
import re
from typing import Dict, Any

def check_firewall_status():
    """
    Perform a comprehensive audit of Windows Firewall status and configuration.
    Checks all profiles, rules, logging settings, and current connections.
    """
    logging.info("\n" + "="*50)
    logging.info("STARTING WINDOWS FIREWALL COMPREHENSIVE AUDIT")
    logging.info("="*50 + "\n")
    
    try:
        # Check basic firewall status for all profiles
        check_firewall_profiles()
        
        # Check global firewall settings
        check_global_firewall_settings()
        
        # Check firewall logging configuration
        check_firewall_logging()
        
        # List all firewall rules
        list_firewall_rules()
        
        # Check current firewall state and connections
        check_current_firewall_state()
        
        # Check domain/private/public profile differences
        compare_profiles()
        
        logging.info("\n" + "="*50)
        logging.info("FIREWALL AUDIT COMPLETED SUCCESSFULLY")
        logging.info("="*50)
        
    except Exception as e:
        logging.error(f"Firewall audit failed: {e}", exc_info=True)

def check_firewall_profiles():
    """Check status of all firewall profiles (Domain, Private, Public)"""
    logging.info("\n=== FIREWALL PROFILE STATUS ===")
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles"], 
            capture_output=True, 
            text=True,
            check=True
        )
        profile_data = parse_profile_output(result.stdout)
        
        for profile, status in profile_data.items():
            logging.info(f"\n{profile.upper()} PROFILE:")
            for key, value in status.items():
                logging.info(f"{key.replace('_', ' ').title()}: {value}")
                
        return profile_data
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get firewall profiles: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error checking profiles: {e}")

def parse_profile_output(output: str) -> Dict[str, Dict[str, str]]:
    """Parse the netsh advfirewall show allprofiles output"""
    profiles = {}
    current_profile = None
    
    for line in output.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Domain Profile'):
            current_profile = 'domain'
            profiles[current_profile] = {}
        elif line.startswith('Private Profile'):
            current_profile = 'private'
            profiles[current_profile] = {}
        elif line.startswith('Public Profile'):
            current_profile = 'public'
            profiles[current_profile] = {}
        elif current_profile and ':' in line:
            key, value = [part.strip() for part in line.split(':', 1)]
            profiles[current_profile][key] = value
            
    return profiles

def check_global_firewall_settings():
    """Check firewall settings for current profile"""
    logging.info("\n=== GLOBAL FIREWALL SETTINGS ===")
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "currentprofile"],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("\nCurrent Profile Settings:\n" + result.stdout)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "Unknown error (empty stderr)"
        logging.error(f"Failed to get global settings: {error_message}")
    except Exception as e:
        logging.error(f"Unexpected error checking global settings: {e}")

def check_firewall_logging():
    """Check firewall logging settings"""
    logging.info("\n=== FIREWALL LOGGING CONFIGURATION ===")
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "currentprofile", "logging"], 
            capture_output=True, 
            text=True,
            check=True
        )
        
        logging.info("Firewall Logging Settings:\n" + result.stdout)
        
        # Extract log paths
        log_paths = re.findall(r"Log file location:\s*(.+?)\s*$", result.stdout, re.MULTILINE)
        if log_paths:
            logging.info(f"\nFirewall log files can be found at: {', '.join(log_paths)}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get logging settings: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error checking logging: {e}")

def list_firewall_rules():
    """List all firewall rules with key details"""
    logging.info("\n=== FIREWALL RULES AUDIT ===")
    try:
        # Get all firewall rules
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], 
            capture_output=True, 
            text=True,
            check=True
        )
        
        # Count rules by direction and action
        rules = result.stdout.split('Rule Name:')
        enabled_rules = [r for r in rules if 'Enabled:             Yes' in r]
        
        logging.info(f"Total firewall rules: {len(rules)-1}")
        logging.info(f"Enabled firewall rules: {len(enabled_rules)}")
        
        # Show some example rules
        logging.info("\nSample of firewall rules (first 5):")
        for rule in rules[1:6]:
            logging.info("\n" + rule.strip())
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get firewall rules: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error checking rules: {e}")

def check_current_firewall_state():
    """Check current firewall state and active connections"""
    logging.info("\n=== CURRENT FIREWALL STATE ===")
    try:
        # Check active firewall ports
        result = subprocess.run(
            ["netsh", "advfirewall", "monitor", "show", "firewall"], 
            capture_output=True, 
            text=True,
            check=True
        )
        logging.info("Active Firewall State:\n" + result.stdout)
        
        # Check current connections (requires admin)
        try:
            result = subprocess.run(
                ["netstat", "-ano"], 
                capture_output=True, 
                text=True,
                check=True
            )
            logging.info("\nCurrent Network Connections:\n" + result.stdout)
        except subprocess.CalledProcessError:
            logging.warning("Could not get network connections (admin rights needed)")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get firewall state: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error checking state: {e}")

def compare_profiles():
    """Compare settings between different firewall profiles"""
    logging.info("\n=== PROFILE COMPARISON ===")
    try:
        profiles = ['domain', 'private', 'public']
        settings = {}
        
        for profile in profiles:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", profile, "profile"], 
                capture_output=True, 
                text=True,
                check=True
            )
            settings[profile] = parse_profile_settings(result.stdout)
        
        # Compare key settings
        logging.info("\nProfile Settings Comparison:")
        for setting in ['Firewall Policy', 'Inbound User Notification', 'Unicast Response']:
            logging.info(f"\n{setting}:")
            for profile in profiles:
                logging.info(f"  {profile.title()}: {settings[profile].get(setting, 'N/A')}")
                
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to compare profiles: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error comparing profiles: {e}")

def parse_profile_settings(output: str) -> Dict[str, str]:
    """Parse individual profile settings"""
    settings = {}
    for line in output.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = [part.strip() for part in line.split(':', 1)]
            settings[key] = value
    return settings

if __name__ == "__main__":
    # Configure logging to audit.log
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('audit.log', mode='a'),  # Always append to audit.log
            logging.StreamHandler()
        ]
    )
    
    check_firewall_status()