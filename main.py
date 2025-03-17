import argparse
from audits import (
    user_audit
)

def main():
    parser = argparse.ArgumentParser(description="Windows Auditing Tool for System Security & Compliance")
    parser.add_argument("--all", action="store_true", help="Run all audits")
    parser.add_argument("--users", action="store_true", help="Audit user accounts")
    args = parser.parse_args()

    if args.all or args.users:
        print("\n[+] Running User Audit...")
        user_audit.run_audit()

if __name__ == "__main__":
    main()