import argparse
import modules.system_info as sys_info
import modules.firewall_check as firewall
import modules.antivirus_check as antivirus
import modules.patch_management as patch
import modules.startup_review as startup
import modules.services as service
import modules.installed_applications as applications
import modules.scheduled_task as schedule
import modules.user_accounts as accounts
import modules.remote_access as remote
from modules.logging import setup_logging, clear_logs

def perform_all_audits():
    """Perform all available audits"""
    sys_info.get_system_info()
    firewall.check_firewall_status()
    antivirus.check_antivirus()
    patch.check_patch_status()
    startup.check_startup_apps()
    service.audit_services()
    applications.list_installed_apps()
    schedule.check_scheduled_tasks()
    accounts.audit_user_accounts()
    remote.audit_remote_access()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Windows Security Audit Tool')
    parser.add_argument('--clear-logs', action='store_true', help='Clear the audit log file')
    parser.add_argument('--all', action='store_true', help='Perform all available audits')
    parser.add_argument('--system', action='store_true', help='Perform system information audit')
    parser.add_argument('--firewall', action='store_true', help='Perform firewall audit')
    parser.add_argument('--antivirus', action='store_true', help='Perform antivirus audit')
    parser.add_argument('--patch', action='store_true', help='Perform patch management audit')
    parser.add_argument('--startup', action='store_true', help='Perform Startup Review audit')
    parser.add_argument('--service', action='store_true', help='Perform service audit')
    parser.add_argument('--applications', action='store_true', help='Perform Applications audit')
    parser.add_argument('--schedule', action='store_true', help='Perform Schedule Task audit')
    parser.add_argument('--accounts', action='store_true', help='Perform User Accounts audit')
    parser.add_argument('--remote', action='store_true', help='Perform Remote Access audit')
    
    
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
        if args.patch:
            patch.check_patch_status()
        if args.startup:
            startup.check_startup_apps()
        if args.service:
            service.audit_services()
        if args.applications:
            applications.list_installed_apps()
        if args.schedule:
            schedule.check_scheduled_tasks()
        if args.accounts:
            accounts.audit_user_accounts()
        if args.remote:
            remote.audit_remote_access()
    
    print("Windows Audit Completed.")

if __name__ == "__main__":
    main()