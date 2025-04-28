import subprocess
import logging

def audit_remote_access():
    logging.info("Checking remote access settings...")
    try:
        # Run netstat to get all active connections and listening ports
        result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
        
        # Check for common remote access ports (SSH, RDP, HTTP/HTTPS)
        remote_ports = ['22', '3389', '80', '443']
        logging.info("Checking for open remote access ports (SSH, RDP, HTTP, HTTPS)...")
        
        lines = result.stdout.splitlines()
        listening_ports = []
        established_connections = []

        # Separate listening ports and established connections
        for line in lines:
            if 'LISTEN' in line:
                listening_ports.append(line)
            if 'ESTABLISHED' in line:
                established_connections.append(line)
        
        # Log listening ports and established connections
        if listening_ports:
            logging.info("Listening Ports:")
            for port in listening_ports:
                if any(remote_port in port for remote_port in remote_ports):
                    logging.info(port)
                else:
                    logging.debug(port)
        
        if established_connections:
            logging.info("Established Connections:")
            for connection in established_connections:
                logging.info(connection)

        # If no relevant ports found, log a warning
        if not listening_ports and not established_connections:
            logging.warning("No remote access connections found.")
        
    except Exception as e:
        logging.error(f"Failed to check remote access: {e}")