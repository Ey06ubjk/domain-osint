import nmap, socket, sys

# Common ports and their descriptions for TCP
tcp_port_descriptions = {
    21: "FTP - File Transfer Protocol",
    22: "SSH - Secure Shell",
    23: "Telnet - Unencrypted text communications",
    25: "SMTP - Simple Mail Transfer Protocol",
    80: "HTTP - Hypertext Transfer Protocol",
    110: "POP3 - Post Office Protocol version 3",
    143: "IMAP - Internet Message Access Protocol",
    443: "HTTPS - HTTP Secure",
    445: "SMB - Server Message Block",
    3389: "RDP - Remote Desktop Protocol",
    8080: "HTTP Alternate - often used for Web proxies or additional Web servers",
    2222: "DirectAdmin’s default port"
}

# Common ports and their descriptions for UDP
udp_port_descriptions = {
    53: "DNS - Domain Name System",
    67: "DHCP - Dynamic Host Configuration Protocol (Server)",
    68: "DHCP - Dynamic Host Configuration Protocol (Client)",
    69: "TFTP - Trivial File Transfer Protocol",
    123: "NTP - Network Time Protocol",
    161: "SNMP - Simple Network Management Protocol",
    500: "ISAKMP - Internet Security Association and Key Management Protocol",
    995: "POP3S - POP3 over SSL",
    1900: "SSDP - Simple Service Discovery Protocol",
    5353: "mDNS - Multicast DNS",
    11211: "Memcached - Memory object caching system"
}

def resolve_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def scan_domain(domain):
    scanner = nmap.PortScanner()
    ip_address = resolve_domain(domain)
    if ip_address is None:
        print(f"Error: Could not resolve domain {domain}")
        sys.exit(1)

    print(f"Nmap results for: {domain} ({ip_address})")
    
    # TCP scan
    print("\nProtocol: TCP")
    tcp_ports = ','.join(map(str, tcp_port_descriptions.keys()))
    scanner.scan(ip_address, tcp_ports, '-sS')
    display_results(scanner, "tcp")

    # UDP scan
    print("\nProtocol: UDP")
    udp_ports = ','.join(map(str, udp_port_descriptions.keys()))
    scanner.scan(ip_address, udp_ports, '-sU')
    display_results(scanner, "udp")

def display_results(scanner, protocol):
    for host in scanner.all_hosts():
        if scanner[host].state() == 'up':
            for proto in scanner[host].all_protocols():
                if proto == protocol:
                    lport = scanner[host][proto].keys()
                    for port in sorted(lport):
                        port_info = scanner[host][proto][port]
                        state = port_info['state']
                        description = (tcp_port_descriptions if protocol == 'tcp' else udp_port_descriptions).get(port, "No description available")
                        print(f"Port: {port}\tState: {state} - {description}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    scan_domain(domain)