import argparse, logging, threading, requests, socket, idna, dns.resolver
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Subdomain Enumeration and Analysis Tool')
    parser.add_argument('-d', '--domain', required=True, help='The target domain to analyze')
    parser.add_argument('--cname', action='store_true', help='CNAME lookup for subdomain takeover (Placeholder)')
    parser.add_argument('--resolve', action='store_true', help='Resolve DNS names.')
    return parser.parse_args()

def read_predefined_subdomains(file_path):
    with open(file_path, 'r') as file:
        subdomains = {line.strip() for line in file if line.strip()}
    return subdomains

def resolve_dns(domain):
    try:
        # Ensure the domain name is not empty
        if not domain:
            raise ValueError("Domain name is empty")

        ascii_domain = idna.encode(domain).decode('ascii') 
        ip_addresses = socket.gethostbyname_ex(ascii_domain)[2]  # Resolve the domain name to IP addresses
        #print('dns resolve')
        #print(ip_addresses)
        return ip_addresses
        
    except ValueError as e:
        return []
    except UnicodeError as e:
        return []
    except socket.gaierror as e:
        pass

def fetch_cname(domain):
    try:
        cname_records = dns.resolver.resolve(domain, 'CNAME')
        return [str(record.target) for record in cname_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []
    except Exception as e:
        return []


def fetch_subdomains_crt(domain, timeout=2):
    """Fetch subdomains for a given domain using crt.sh and return as a set."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        subdomains = set(sub.replace('*', '').strip() for data in response.json() for sub in data['name_value'].split('\n') if sub)
        return subdomains
    except requests.RequestException as e:
        logging.debug(f'Error fetching subdomains: {e}')
        return set()

def fetch_subdomains_alienvault(domain, timeout=2, retries=1):
    """Fetch subdomains for a given domain using AlienVault OTX."""
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            subdomains = {data['hostname'] for data in response.json().get('passive_dns', []) if 'hostname' in data}
            return subdomains
        except requests.Timeout:
            logging.debug(f'Attempt {attempt + 1} timed out. Retrying...')
            timeout *= 2  # Increase timeout for the next attempt
        except requests.RequestException as e:
            logging.debug(f'Error fetching subdomains from AlienVault: {e}')
            return set()
    logging.debug('Max retries exceeded for AlienVault.')
    return set()

def fetch_subdomains_dnsrepo(domain, timeout=2):
    """Fetch subdomains for a given domain using dnsrepo."""
    url = f"https://dnsrepo.noc.org/?search={domain}"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        subdomains = set()
        for a in soup.find_all('a', href=True):
            link = a['href']
            if "?domain=" in link and link.endswith(f'{domain}.'):
                sub = link.split('/?domain=')[1].rstrip('.')
                subdomains.add(sub)
        return subdomains
    except requests.RequestException as e:
        logging.debug(f'Error fetching subdomains from dnsrepo: {e}')
        return set()

def fetch_subdomains_dnsdumpster(domain, timeout=2):
    """Fetch subdomains for a given domain using DNSdumpster (via HackerTarget's API)."""
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for bad responses
        if response.status_code == 200:
            subdomains = set(line.split(",")[0] for line in response.text.splitlines() if line.count('.') > 1)
            return subdomains
        elif response.status_code == 429:
            logging.debug('Too many requests to DNSdumpster API')
            return set()
    except requests.RequestException as e:
        logging.debug(f'Error fetching subdomains from DNSdumpster: {e}')
        return set()

def fetch_subdomains_archive(domain, timeout=2):
    """Fetch subdomains for a given domain using archive.org."""
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for bad responses
        subdomains = set()
        if response.status_code == 200:
            json_data = response.json()
            if json_data:
                for item in json_data[1:]:  # Skip the first item as it is the header
                    subdomain_url = item[2]  # Assuming the URL is in the third column
                    parsed_url = urlparse(f'http://{subdomain_url}')
                    subdomain = parsed_url.hostname
                    if subdomain:  # Ensure it's not None
                        subdomain = subdomain.split(':')[0]  # Remove port number if present
                        subdomains.add(subdomain)
        return subdomains
    except requests.RequestException as e:
        logging.debug(f'Error fetching subdomains from archive.org: {e}')
        return set()

def get_ip_info(ip_address):
    """Get information for an IP address using ipinfo.io."""
    url = f'https://ipinfo.io/{ip_address}/json'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

class SubdomainFinder(threading.Thread):
    def __init__(self, domain, args):
        super().__init__(daemon=True)
        self.domain = domain
        self.args = args
        self.results = set()

    def run(self):
        predefined_subdomains = read_predefined_subdomains('/app/scripts/data/subdomains.txt')
        predefined_subdomains_full = {f"{sub}.{self.domain}" for sub in predefined_subdomains}
        subdomains = set().union(
            fetch_subdomains_crt(self.domain),
            fetch_subdomains_alienvault(self.domain),
            fetch_subdomains_dnsrepo(self.domain),
            fetch_subdomains_dnsdumpster(self.domain),
            fetch_subdomains_archive(self.domain),
            predefined_subdomains_full
        )
        for subdomain in subdomains:
            dns_resolved_ips = resolve_dns(subdomain) if self.args.resolve else []
            cnames = fetch_cname(subdomain) if self.args.cname else []

            # Only print if DNS resolved or HTTP status is Active
            if dns_resolved_ips:
                cname_formatted = ', '.join(cnames) if cnames else 'No CNAME'
                ips_formatted = ', '.join(dns_resolved_ips) if dns_resolved_ips else 'No IPs'

                # Fetch IP info for each resolved IP and format it for printing
                ip_info_messages = []
                for ip in dns_resolved_ips:
                    ip_info = get_ip_info(ip)
                    if ip_info:
                        info_message = f"\nIP: {ip_info.get('ip', 'N/A')} | {ip_info.get('hostname', 'N/A')} | {ip_info.get('org', 'N/A')}"
                        ip_info_messages.append(info_message)
                    else:
                        ip_info_messages.append("No additional IP info found")
                ip_info_formatted = ''.join(ip_info_messages)

                print(f"[Subdomain] {subdomain} [{ips_formatted}] [{cname_formatted}] [{ip_info_formatted}]\n")
                self.results.add(subdomain)
        print(f'[*] Identified {len(self.results)} active subdomain(s).')

def main():
    args = parse_arguments()
    finder = SubdomainFinder(args.domain, args)
    finder.start()
    finder.join()

if __name__ == "__main__":
    main()