import argparse
from audits import (
    user_audit,
    file_audit  # Import the file audit module
)

def main():
    parser = argparse.ArgumentParser(description="Windows Auditing Tool for System Security & Compliance")
    parser.add_argument("--all", action="store_true", help="Run all audits")
    parser.add_argument("--users", action="store_true", help="Audit user accounts")
    parser.add_argument("--files", action="store_true", help="Audit files (Sensitive, Critical, Setuid)")
    
    args = parser.parse_args()

    if args.all or args.users:
        print("\n[+] Running User Audit...")
        user_audit.run_audit()

    if args.all or args.files:
        print("\n[+] Running File Audit...")
        file_audit.audit()  # Run the file audit

if __name__ == "__main__":
    main()
