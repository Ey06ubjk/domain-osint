import urllib.request, urllib.error, urllib.parse, ssl, sys

# Client headers to send during the request.
client_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.3',
    'Upgrade-Insecure-Requests': 1
}

# Security headers to be checked
sec_headers = [
    'X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security', 'Content-Security-Policy',
    'Referrer-Policy', 'Permissions-Policy', 'Cross-Origin-Embedder-Policy', 
    'Cross-Origin-Resource-Policy', 'Cross-Origin-Opener-Policy'
]

def parse_headers(hdrs):
    return dict((x.lower(), y) for x, y in hdrs)

def main(url):
    print(f"Analyzing headers of {url}\n")

    # Create request object
    request = urllib.request.Request(url, headers=client_headers)
    # Disable SSL verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(request, timeout=10, context=context)
        headers = parse_headers(response.getheaders())
        found_headers_count = 0
        missing_headers_count = 0

        for h in sec_headers:
            h_lower = h.lower()
            if h_lower in headers:
                found_headers_count += 1
                print(f"[*] Header {h} is present! (Value: {headers[h_lower]})")
            else:
                missing_headers_count += 1
                print(f"[!] Missing security header: {h}")
       
        print('--------------------------------------------------------')
        print(f"\nFound {found_headers_count} present security header(s).")
        print(f"Found {missing_headers_count} missing security header(s).")
    except Exception as e:
        print(f"Error analyzing {url}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python shcheck.py <url>")
        sys.exit(1)
    main(sys.argv[1])
