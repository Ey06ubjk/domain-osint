import requests, argparse, os
from dotenv import load_dotenv

# Loading .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_api_credits(api_key):
    url = f"https://api.hunter.io/v2/account?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        account_info = data.get('data')
        reset_date = data.get('data', {}).get('reset_date')
        request = account_info.get('requests', {}).get('searches', {}).get('used')
        return request, reset_date
    else:
        print(f"Error fetching account info: {response.status_code}")
        return None

def get_hunter_emails(domain, api_key):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        emails = [contact['value'] for contact in data.get('data', {}).get('emails', [])]
        pattern = data.get('data', {}).get('pattern', 'Not available')
        return pattern, emails
    else:
        print(f"Error from Hunter.io: {response.status_code}")
        return None, []

def get_prospeo_emails(domain, api_key):
    url = "https://api.prospeo.io/domain-search"
    headers = {
        'Content-Type': 'application/json',
        'X-KEY': api_key
    }
    data = {
        'company': domain,
        'limit': 100
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        emails = [email_info['email'] for email_info in data.get('response', {}).get('email_list', [])]
        return emails
    else:
        print(f"Error from Prospeo: {response.status_code}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Retrieve emails from multiple sources for a given domain.')
    parser.add_argument('-d', '--domain', required=True, help='Domain name to query emails')
    args = parser.parse_args()

    api_key_prospeo = os.getenv('api_key_prospeo')
    api_key_hunter = os.getenv('api_key_hunter')

    # Fetch emails from Hunter.io and Prospeo
    email_pattern, hunter_emails = get_hunter_emails(args.domain, api_key_hunter)
    prospeo_emails = get_prospeo_emails(args.domain, api_key_prospeo)
    combined_emails = list(set(hunter_emails + prospeo_emails))    # Combine and deduplicate email lists

    if email_pattern:
        print(f"Email pattern for {args.domain}: {email_pattern}@{args.domain}\n")
    for email in combined_emails:
        print(email)

    used_credits, reset_date = get_api_credits(api_key_hunter)
    if used_credits is not None:
        remaining_credits = 25 - used_credits
        print(f"\nYou have {remaining_credits} searches left this month of 25.\nSame domain searches won't consume extra credits. Reset date: {reset_date}")
    else:
        print("Unable to fetch Hunter.io search credits. Exiting.")
        return

if __name__ == "__main__":
    main()