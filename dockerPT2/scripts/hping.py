import subprocess, argparse

def run_hping3(domain):
    # Construct the hping3 command
    command = [
        'hping3',
        '--count', '2',
        '-t', '128',
        '--syn',
        '-p', '80',
        '--tcp-timestamp',
        domain
    ]
    try:
        # Execute the command
        result = subprocess.run(command, text=True, capture_output=True, check=True)

        # Process the output
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if 'HPING' in line or ('len=' in line and 'seq=1' in line) or 'System uptime seems' in line:
                print(line.strip())  # Strips any leading/trailing whitespace before printing

    except subprocess.CalledProcessError as e:
        print(f"Error executing hping3: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Create parser and add command line argument for domain
    parser = argparse.ArgumentParser(description='Run hping3 to get network info and system uptime.')
    parser.add_argument('-d', '--domain', type=str, required=True, help='Domain to scan')

    # Parse arguments
    args = parser.parse_args()

    # Run the hping3 function with the provided domain
    run_hping3(args.domain)

if __name__ == '__main__':
    main()
