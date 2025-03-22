import os
import pywintypes
import subprocess  # Import subprocess
import win32api
import win32file
import time  # Import time

def scan_sensitive_files():
    # List of sensitive files commonly found on Windows
    sensitive_paths = [
        'C:\\Windows\\System32\\config\\SAM',  # Security Account Manager (SAM)
        'C:\\Windows\\System32\\config\\SYSTEM',  # System settings file
        'C:\\Windows\\System32\\config\\SECURITY'  # Security settings file
    ]
    sensitive_files = [path for path in sensitive_paths if os.path.exists(path)]
    return sensitive_files

def detect_critical_file_changes():
    # Critical system files that are vital for Windows security
    critical_files = [
        'C:\\Windows\\System32\\config\\SAM',
        'C:\\Windows\\System32\\config\\SYSTEM',
        'C:\\Windows\\System32\\config\\SECURITY'
    ]
    changed_files = []
    for file_path in critical_files:
        try:
            stat_info = os.stat(file_path)
            
            known_time = 1640995200  # Replace with your known timestamp
            if stat_info.st_mtime > known_time:  # Compare file modification time
                changed_files.append(file_path)
        except FileNotFoundError:
            pass
    return changed_files

def find_setuid_files(start_path): 
    # Windows does not have a direct equivalent of the setuid bit.
    # However, we can search for files with the 'System' or 'Hidden' attributes.
    setuid_files = []

    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                attrs = win32api.GetFileAttributes(file_path)
                # Check if file has System or Hidden attributes (like setuid in Linux)
                if attrs & (win32file.FILE_ATTRIBUTE_SYSTEM | win32file.FILE_ATTRIBUTE_HIDDEN):
                    setuid_files.append(file_path)
            except (OSError, PermissionError):
                # Skip the file if it can't be accessed due to permission errors or being used by another process
                pass
            except pywintypes.error as e:
                # Handle the specific error where the file is being used by another process
                if e.winerror == 32:  # Error code 32: The process cannot access the file because it is being used by another process
                    print(f"WARNING: File '{file_path}' is in use by another process and was skipped.")
                else:
                    raise  # Raise any other exceptions
    return setuid_files

def audit():
    # Accept folder path from user input
    folder_path = input("Please enter the folder path to audit (e.g., C:\\My File): ").strip()

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"ERROR: The folder path '{folder_path}' does not exist.")
        return

    print("\n\nScanning for sensitive files:")
    sensitive_files = scan_sensitive_files()
    print(sensitive_files)

    print("\n\nDetecting changes to critical system files:")
    critical_changes = detect_critical_file_changes()
    print(critical_changes)

    print("\n\nSearching for files with System or Hidden attributes (similar to setuid):")
    setuid_files = find_setuid_files(folder_path)  # Pass the folder path provided by the user
    
    if setuid_files:
        print("Files with System/Hidden attributes found:")
        for file in setuid_files:
            print(file)
    else:
        print("No files with System/Hidden attributes found.")

    print("\n===== AUDIT COMPLETE =====\n")

# Run the audit function

