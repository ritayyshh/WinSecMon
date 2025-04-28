import subprocess
import re
import logging

# Set up logging
#logging.basicConfig(filename='audit.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def list_user_accounts():
    """List all local user accounts on the system"""
    try:
        output = subprocess.check_output(
            ['powershell', '-command', 'Get-LocalUser | Select-Object Name,Enabled,LastLogon | Format-Table -HideTableHeaders'],
            text=True
        )
        users = []
        for line in output.splitlines():
            if line.strip():
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 2:
                    users.append({
                        'name': parts[0],
                        'enabled': parts[1],
                        'last_logon': parts[2] if len(parts) > 2 else 'Never'
                    })
        return users
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing user accounts: {e}")
        return f"Error listing user accounts: {e}"

def check_password_policies():
    """Check password policies and account status"""
    try:
        # Get password policy
        policy = subprocess.check_output(
            ['powershell', '-command', 'net accounts'],
            text=True
        )
        
        # Get users with password never expires
        never_expires = subprocess.check_output(
            ['powershell', '-command', 'Get-LocalUser | Where-Object {$_.PasswordNeverExpires -eq $true} | Select-Object Name'],
            text=True
        )
        
        # Get disabled accounts
        disabled_accounts = subprocess.check_output(
            ['powershell', '-command', 'Get-LocalUser | Where-Object {$_.Enabled -eq $false} | Select-Object Name'],
            text=True
        )
        
        return policy, never_expires, disabled_accounts
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking password policies: {e}")
        return f"Error checking password policies: {e}"

def list_admin_users():
    """List users with administrative privileges"""
    try:
        admins = subprocess.check_output(
            ['powershell', '-command', 'Get-LocalGroupMember -Group "Administrators" | Select-Object Name,PrincipalSource | Format-Table -HideTableHeaders'],
            text=True
        )
        admin_list = []
        for line in admins.splitlines():
            if line.strip():
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 2:
                    admin_list.append({
                        'name': parts[0],
                        'source': parts[1]
                    })
        return admin_list
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing admin users: {e}")
        return f"Error listing admin users: {e}"

def review_account_history():
    """Review recent account login history"""
    try:
        # Get last login times (limited to 10 for brevity)
        history = subprocess.check_output(
            ['powershell', '-command', 'Get-EventLog -LogName Security -InstanceId 4624 -Newest 10 | Select-Object TimeGenerated,Message | Format-Table -Wrap -AutoSize'],
            text=True
        )
        return history
    except subprocess.CalledProcessError as e:
        logging.error(f"Error reviewing account history: {e}")
        return f"Error reviewing account history: {e}"

def audit_user_accounts():
    """Run all audit functions and display results"""
    logging.info("=== Windows User Account Audit ===")
    
    logging.info("\n[1] User Accounts:")
    users = list_user_accounts()
    if isinstance(users, list):
        for user in users:
            logging.info(f"User: {user['name']}, Enabled: {user['enabled']}, Last Logon: {user['last_logon']}")
    else:
        logging.error(users)
    
    logging.info("\n[2] Password Policies and Account Status:")
    policy, never_expires, disabled_accounts = check_password_policies()
    logging.info("Password Policies:")
    logging.info(policy)
    logging.info("\nUsers with Password Never Expires:")
    logging.info(never_expires)
    logging.info("\nDisabled Accounts:")
    logging.info(disabled_accounts)
    
    logging.info("\n[3] Users with Administrative Privileges:")
    admins = list_admin_users()
    if isinstance(admins, list):
        for admin in admins:
            logging.info(f"Admin: {admin['name']} (Source: {admin['source']})")
    else:
        logging.error(admins)
    
    logging.info("\n[4] Recent Account Login History (last 10 events):")
    history = review_account_history()
    logging.info(history)

if __name__ == "__main__":
    audit_user_accounts()