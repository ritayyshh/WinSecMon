import subprocess
import json
from tabulate import tabulate


def run_powershell(cmd):
    """Runs a PowerShell command safely with a timeout."""
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"ERROR: Command timed out: {cmd}")
        return ""
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return ""


def list_user_accounts():
    """Lists all local user accounts."""
    print("[+] Listing all user accounts...")
    cmd = "Get-LocalUser | Select-Object Name, Enabled, LastLogon | ConvertTo-Json"
    output = run_powershell(cmd)

    try:
        users = json.loads(output) if output else []
        return users if isinstance(users, list) else [users]
    except json.JSONDecodeError:
        print("ERROR: Failed to parse user list.")
        return []


def check_password_policy():
    """Checks Windows password policies."""
    print("[+] Checking password policies...")
    return run_powershell("net accounts")


def list_admin_users():
    """Lists users with admin privileges."""
    print("[+] Listing administrator users...")
    cmd = "Get-LocalGroupMember -Group Administrators | Select-Object Name | ConvertTo-Json"
    output = run_powershell(cmd)

    try:
        admins = json.loads(output) if output else []
        return admins if isinstance(admins, list) else [admins]
    except json.JSONDecodeError:
        print("ERROR: Failed to parse admin users.")
        return []


def check_password_strength():
    """Checks for weak and expired passwords."""
    print("[+] Checking user password strength...")

    weak_passwords = []
    expired_passwords = []

    cmd = """
    Get-WmiObject Win32_UserAccount | Select-Object Name, PasswordRequired, PasswordExpires | ConvertTo-Json
    """
    output = run_powershell(cmd)

    try:
        users = json.loads(output) if output else []
        if not isinstance(users, list):
            users = [users]

        for user in users:
            name = user.get("Name", "Unknown")
            password_required = user.get("PasswordRequired", True)
            password_expires = user.get("PasswordExpires", False)

            if not password_required:
                weak_passwords.append(name)
            if not password_expires:
                expired_passwords.append(name)

    except json.JSONDecodeError:
        print("ERROR: Failed to parse password info.")

    return weak_passwords, expired_passwords


def get_account_creation_dates():
    """Fetches account creation history (Event ID 4720)."""
    print("[+] Fetching account creation history...")

    cmd = """
    Get-WinEvent -LogName Security -FilterXPath "*[System[(EventID=4720)]]" |
    Select-Object TimeCreated, @{Name='UserName';Expression={$_.Properties[0].Value}} | ConvertTo-Json
    """
    output = run_powershell(cmd)

    creation_history = []
    try:
        events = json.loads(output) if output else []
        if isinstance(events, dict):
            events = [events]

        for event in events:
            creation_history.append([event.get("UserName", "Unknown"), event.get("TimeCreated", "Unknown")])

    except json.JSONDecodeError:
        print("ERROR: Failed to parse creation history.")

    return creation_history


def run_audit():
    """Runs all user audit checks and displays results in a formatted table."""
    print("\n===== WINDOWS USER AUDIT REPORT =====\n")

    users = list_user_accounts()
    user_table = [[user.get("Name", "Unknown"), user.get("Enabled"), user.get("LastLogon", "Never")] for user in users]
    print(tabulate(user_table, headers=["User Name", "Enabled", "Last Logon"], tablefmt="grid"))

    print("\n[Password Policy]")
    print(check_password_policy())

    admin_users = list_admin_users()
    admin_table = [[admin.get("Name", "Unknown")] for admin in admin_users]
    print("\n[Users with Administrative Privileges]")
    print(tabulate(admin_table, headers=["Admin Users"], tablefmt="grid"))

    weak_passwords, expired_passwords = check_password_strength()

    print("\n[Users with Weak Passwords]")
    if weak_passwords:
        print(tabulate([[user] for user in weak_passwords], headers=["User Name"], tablefmt="grid"))
    else:
        print("No weak passwords found.")

    print("\n[Users with Expired Passwords]")
    if expired_passwords:
        print(tabulate([[user] for user in expired_passwords], headers=["User Name"], tablefmt="grid"))
    else:
        print("No expired passwords found.")

    creation_history = get_account_creation_dates()
    print("\n[User Account Creation History]")
    if creation_history:
        print(tabulate(creation_history, headers=["User Name", "Creation Date"], tablefmt="grid"))
    else:
        print("No account creation history available.")

    print("\n===== AUDIT COMPLETE =====\n")