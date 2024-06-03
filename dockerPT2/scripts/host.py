import subprocess, sys

# The domain to query, taken from the command line arguments
if len(sys.argv) != 2:
    print("Usage: python host.py <domain>")
    sys.exit(1)
domain = sys.argv[1]

record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'SOA', 'CNAME', 'DS', 'DNSKEY']   # List of DNS record types to query

def query_dns(domain, record_type):
    """
    Query the DNS for the given domain and record type using the host command.
    Returns None if the query fails, otherwise returns the output.
    """
    try:
        result = subprocess.run(['host', '-t', record_type, domain], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        return output if output else f"No {record_type} records found."
    except subprocess.CalledProcessError:
        return None

def main():
    dns_results = {}
    failed = False

    # Perform DNS queries for each record type and store the results
    for record_type in record_types:
        output = query_dns(domain, record_type)
        if output is None:
            failed = True
        else:
            dns_results[record_type] = output

    if failed:
        print("DNS lookup script failed.")   # If any query failed, print only the failure message.
    else:
        # If all queries succeeded, print the results.
        print(f'DNS lookup for {domain}')
        for record_type, output in dns_results.items():
            print(f"\n=== {record_type} Records ===\n{output}")

if __name__ == "__main__":
    main()
