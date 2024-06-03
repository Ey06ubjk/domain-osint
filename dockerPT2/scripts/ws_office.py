import dns.resolver, argparse, requests, argparse

# Check if a domain is using Google Workspace by looking up its MX records.
def check_google_workspace(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        google_records = [str(record.exchange).lower() for record in records if 'google' in str(record.exchange).lower()]
        return {
            'Domain': domain,
            'UsingGoogleWorkspace': bool(google_records),
            'GoogleMXRecords': google_records
        }
    except dns.resolver.NoAnswer:
        return {
            'Domain': domain,
            'UsingGoogleWorkspace': False,
            'GoogleMXRecords': [],
            'Error': 'No MX records found'
        }
    except Exception as e:
        return {
            'Domain': domain,
            'UsingGoogleWorkspace': False,
            'GoogleMXRecords': [],
            'Error': str(e)
        }

# Print the status of Google Workspace usage for a domain.
def print_status_info_ws(result):
    if result['UsingGoogleWorkspace']:
        print('-----------------------------------------------------')
        print(f"\n[*]This domain is using Google Workspace: {result['Domain']}")
        print("Google MX records:")
        for mx_record in result['GoogleMXRecords']:
            print(f"  {mx_record}")
    else:
        print('-----------------------------------------------------')
        print(f"\n[*]No Google Workspace records found for {result['Domain']}.")
        if 'Error' in result:
            print(f"\nError: {result['Error']}")

# Make a request to check if a domain is associated with Office 365.
def make_request_office(target):
    url = 'https://login.microsoftonline.com/getuserrealm.srf'
    params = {'login': f'username@{target}', 'json': '1'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Print the status of Office 365 usage for a domain.
def print_status_info_office(response_json):
    namespace_type = response_json.get('NameSpaceType', 'Unknown')
    domain_status = {
        'Managed': '[*]This domain is Managed (using O365).\n',
        'Federated': '[*]This domain is Federated.\n',
        'Unknown': '[*]No O365 service could be identified for this domain, or it was entered incorrectly.\n',
    }.get(namespace_type, '[*]No O365 status could be found, or there was an error\n')

    print(domain_status)
    for key in ['CloudInstanceIssuerUri', 'CloudInstanceName', 'DomainName', 'FederationBrandName']:
        if key in response_json:
            print(f"{key}: \"{response_json[key]}\"")

def main():
    parser = argparse.ArgumentParser(description='Checks to see if an O365 instance is associated with a domain.')
    parser.add_argument('-d', '--domain', help='Specifies the domain to be checked', required=True)
    args = parser.parse_args()

    try:
        data = make_request_office(args.domain)
        print_status_info_office(data)
    except requests.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
    except requests.ConnectionError:
        print("Error Connecting to the server.")
    except requests.Timeout:
        print("Timeout Error.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    result = check_google_workspace(args.domain)
    print_status_info_ws(result)

if __name__ == "__main__":
    main()