import subprocess, argparse

def run_sslscan(domain):
    # Define the command to run sslscan with specific options
    command = [
        'sslscan', '--no-cipher-details', '--no-ciphersuites', '--no-compression', 
        '--no-fallback', '--no-groups', '--no-renegotiation', '--no-colour', domain
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check if the command was executed successfully
    if result.returncode != 0:
        print("Error running sslscan:")
        print(result.stderr)
        return
    
    # Parse the output to extract SSL/TLS protocols part
    output = result.stdout
    start = output.find("SSL/TLS Protocols:")
    end = output.find("SSL Certificate:", start)

    # Adjust the end point if 'SSL Certificate:' is not found
    if end == -1:
        end = None  # This means slicing till the end of the string if 'SSL Certificate:' is not found.
    
    # Print the SSL/TLS protocols part
    if start != -1:
        tls_protocols_section = output[start:end].strip()
        filtered_lines = [line.strip() for line in tls_protocols_section.split('\n') if line.strip()]
        heartbleed_index = next((i for i, line in enumerate(filtered_lines) if "Heartbleed:" in line), None)
        if heartbleed_index is not None:
            tls_protocols = '\n'.join(filtered_lines[:heartbleed_index])
            heartbleed_section = '\n'.join(filtered_lines[heartbleed_index:])
            clean_section = tls_protocols + '\n\n' + heartbleed_section
        else:
            clean_section = '\n'.join(filtered_lines)

        print(clean_section)
    else:
        print("Could not find the TLS protocols section in the sslscan output.")

def main():
    parser = argparse.ArgumentParser(description='Run sslscan with specific options and parse the output.')
    parser.add_argument('-d', '--domain', required=True, help='The domain to scan with sslscan.')
    args = parser.parse_args()
    run_sslscan(args.domain)

if __name__ == "__main__":
    main()