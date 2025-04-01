import argparse
import modules.system_info as sys_info
import modules.firewall_check as firewall
import modules.antivirus_check as antivirus
from modules.logging import setup_logging, clear_logs

def perform_all_audits():
    """Perform all available audits"""
    sys_info.get_system_info()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Windows Security Audit Tool')
    parser.add_argument('--clear-logs', action='store_true', help='Clear the audit log file')
    parser.add_argument('--all', action='store_true', help='Perform all available audits')
    parser.add_argument('--system', action='store_true', help='Perform system information audit')
    parser.add_argument('--firewall', action='store_true', help='Perform firewall audit')
    parser.add_argument('--antivirus', action='store_true', help='Perform antivirus audit')
    
    args = parser.parse_args()
    
    print("Starting Windows Audit...")
    
    if args.all:
        perform_all_audits()
    else:
        if args.system:
            sys_info.get_system_info()
        if args.firewall:
            firewall.check_firewall_status()
        if args.antivirus:
            antivirus.check_antivirus()
    
    print("Windows Audit Completed.")

if __name__ == "__main__":
    main()