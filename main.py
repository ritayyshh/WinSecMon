import argparse
import modules.system_info as sys_info
import modules.firewall_check as firewall
import modules.antivirus_check as antivirus
import modules.Patch_Management as Patch
import modules.Startup_Review as Startup
import modules.Service as service
import modules.Installed_Applications as Applications
import modules.Scheduled_Task as Schedule
from modules.logging import setup_logging, clear_logs

def perform_all_audits():
    """Perform all available audits"""
    sys_info.get_system_info()
    firewall.check_firewall_status()
    antivirus.check_antivirus()
    Patch.check_patch_status()
    Startup.check_startup_apps()
    service.audit_services()
    Applications.list_installed_apps()
    Schedule.check_scheduled_tasks()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Windows Security Audit Tool')
    parser.add_argument('--clear-logs', action='store_true', help='Clear the audit log file')
    parser.add_argument('--all', action='store_true', help='Perform all available audits')
    parser.add_argument('--system', action='store_true', help='Perform system information audit')
    parser.add_argument('--firewall', action='store_true', help='Perform firewall audit')
    parser.add_argument('--antivirus', action='store_true', help='Perform antivirus audit')
    parser.add_argument('--Patch', action='store_true', help='Perform patch management audit')
    parser.add_argument('--Startup', action='store_true', help='Perform Startup Review audit')
    parser.add_argument('--service', action='store_true', help='Perform service audit')
    parser.add_argument('--Applications', action='store_true', help='Perform Applications audit')
    parser.add_argument('--Schedule', action='store_true', help='Perform Schedule Task audit')
    
    
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
        if args.Patch:
            Patch.check_patch_status()
        if args.Startup:
            Startup.check_startup_apps()
        if args.service:
            service.audit_services()
        if args.Applications:
            Applications.list_installed_apps()
        if args.Schedule:
            Schedule.check_scheduled_tasks()    
    
    print("Windows Audit Completed.")

if __name__ == "__main__":
    main()