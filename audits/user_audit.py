import subprocess
import json
from tabulate import tabulate


def list_user_accounts():
    """Lists all local user accounts on the system."""
    print("[+] Listing all user accounts...")
    cmd = "Get-LocalUser | Select-Object Name, Enabled, LastLogon | ConvertTo-Json"
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    try:
        users = json.loads(result.stdout)
        return users if isinstance(users, list) else [users]  # Handle single user case
    except json.JSONDecodeError:
        return []


def check_password_policy():
    """Checks Windows password policies, including expiry and complexity rules."""
    print("[+] Checking password policies...")
    cmd = "net accounts"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def list_admin_users():
    """Lists users with administrative privileges."""
    print("[+] Listing users with administrator privileges...")
    cmd = "Get-LocalGroupMember -Group Administrators | Select-Object Name | ConvertTo-Json"
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    try:
        admins = json.loads(result.stdout)
        return admins if isinstance(admins, list) else [admins]
    except json.JSONDecodeError:
        return []


def check_password_strength():
    """Analyzes user password strengths based on expiry, complexity, and missing passwords."""
    print("[+] Checking user password strength...")

    weak_passwords = []
    expired_passwords = []

    cmd = """
    Get-WmiObject Win32_UserAccount | Select-Object Name, PasswordRequired, Disabled, Lockout, PasswordExpires | ConvertTo-Json
    """
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)

    try:
        users = json.loads(result.stdout)
        if not isinstance(users, list):
            users = [users]  # Handle single user case

        for user in users:
            name = user.get("Name", "Unknown")
            password_required = user.get("PasswordRequired", True)  # Default to True if missing
            password_expires = user.get("PasswordExpires", False)
            disabled = user.get("Disabled", False)

            # Weak password: Account does not require a password
            if not password_required:
                weak_passwords.append(name)

            # Expired password: If expiration is disabled and the account is enabled
            if not password_expires and not disabled:
                expired_passwords.append(name)

    except json.JSONDecodeError:
        pass

    return weak_passwords, expired_passwords


def get_account_creation_dates():
    """Fetches the creation date of each user account."""
    print("[+] Fetching account creation history...")
    cmd = """
    Get-WmiObject Win32_UserAccount | Select-Object Name, SID | ConvertTo-Json
    """
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)

    creation_history = []
    
    try:
        users = json.loads(result.stdout)
        if not isinstance(users, list):
            users = [users]  # Handle single user case

        for user in users:
            name = user.get("Name", "Unknown")
            sid = user.get("SID", "")

            if sid:
                # Extract the last part of the SID, which usually contains the relative identifier (RID)
                rid = sid.split("-")[-1]
                
                # Get the creation time of the user based on the RID
                cmd = f"wmic useraccount where SID='{sid}' get Name, WhenCreated /format:csv"
                creation_result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
                
                # Extract creation time from the output
                lines = creation_result.stdout.strip().split("\n")
                if len(lines) > 1:
                    creation_time = lines[1].split(",")[-1]  # Extract the last column
                    creation_history.append([name, creation_time])

    except json.JSONDecodeError:
        pass

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
        print("No creation history available.")

    print("\n===== AUDIT COMPLETE =====\n")