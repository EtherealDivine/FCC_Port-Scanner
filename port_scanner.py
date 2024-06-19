import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # Function to check if IP address is valid
    def is_valid_ip(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    # Function to check if hostname is valid
    def is_valid_hostname(hostname):
        try:
            socket.gethostbyname(hostname)
            return True
        except socket.error:
            return False

    # Determine if the target is a valid IP address or hostname
    ip_address = None
    hostname = None
    if is_valid_ip(target):
        ip_address = target
    else:
        if is_valid_hostname(target):
            hostname = target
            try:
                ip_address = socket.gethostbyname(target)
            except socket.error:
                return "Error: Invalid hostname"
        else:
            return "Error: Invalid hostname"

    # Scan the ports in the specified range
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    if not verbose:
        return open_ports

    # Verbose output
    if hostname:
        output = f"Open ports for {hostname} ({ip_address})\n"
    else:
        output = f"Open ports for {ip_address}\n"

    output += "PORT     SERVICE\n"
    for port in open_ports:
        service_name = ports_and_services.get(port, "unknown")
        output += f"{port:<9}{service_name}\n"

    return output.strip()
