from flask import Flask, jsonify, render_template, request, send_from_directory, url_for, session
from flask_talisman import Talisman
import subprocess, os, logging, uuid, shlex, re, shutil

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
logging.basicConfig(level=logging.INFO)

# Not very necessary in this use case, but can be very important for other!
Talisman(app, content_security_policy=None, force_https=False, session_cookie_secure=False)


@app.route('/run_checks', methods=['POST'])
def run_checks():
    if request.is_json:
        data = request.get_json()
        domain = data['domain']
        domainorg = data['domainorg']
        page = data['page']
        checkboxes = data.get('checkboxes', {})

        outputs, file_paths = handle_requests(domain, domainorg, checkboxes, page)
        for key, path in file_paths.items():
            file_paths[key] = url_for('download', filename=path.split('/')[-1])

        return jsonify(outputs=outputs, file_paths=file_paths)

def handle_requests(domain, domainorg, checkboxes, page):
    """
    #  Processes domain-specific requests based on form inputs. Checks which operations (e.g., 'host' command,
    #  O365 check) were requested and executes them, saving the outputs to files. Returns dictionaries of outputs
    #  and file paths for each operation performed, allowing these to be used.
    """
    # Initializes dictionaries to hold command outputs and file paths
    outputs = {}
    file_paths = {}
    if page is None:
        page = 1

    if checkboxes.get('checkbox1', False):
        host_output = run_host(domain)
        file_path = save_output_to_file(host_output, 'host')
        outputs['host'] = host_output
        file_paths['host'] = file_path

    if checkboxes.get('checkbox2', False):
        o365_output = run_ws_office(domain)
        file_path = save_output_to_file(o365_output, 'ws_office')
        outputs['ws_office'] = o365_output
        file_paths['ws_office'] = file_path

    if checkboxes.get('checkbox3', False):
        whois_output = run_whois(domain)
        file_path = save_output_to_file(whois_output, 'whois')
        outputs['whois'] = whois_output
        file_paths['whois'] = file_path

    if checkboxes.get('checkbox4', False):
        subscaper_output = run_subscraper(domain)
        file_path = save_output_to_file(subscaper_output, 'subscraper')
        outputs['subscraper'] = subscaper_output
        file_paths['subscraper'] = file_path

    if checkboxes.get('checkbox5', False):
        wafw00f_output = run_wafw00f(domain)
        file_path = save_output_to_file(wafw00f_output, 'wafw00f')
        outputs['wafw00f'] = wafw00f_output
        file_paths['wafw00f'] = file_path

    if checkboxes.get('checkbox6', False):
        shcheck_output = run_shcheck(domain)
        file_path = save_output_to_file(shcheck_output, 'shcheck')
        outputs['shcheck'] = shcheck_output
        file_paths['shcheck'] = file_path

    if checkboxes.get('checkbox7', False):
        wpscan_output = run_wpscan(domain)
        file_path = save_output_to_file(wpscan_output, 'wpscan')
        outputs['wpscan'] = wpscan_output
        file_paths['wpscan'] = file_path

    if checkboxes.get('checkbox8', False):
        username_output = run_username(domainorg, page)
        file_path = save_output_to_file(username_output, 'username')
        outputs['username'] = username_output
        file_paths['username'] = file_path

    if checkboxes.get('checkbox9', False):
        email_output = run_email(domain)
        file_path = save_output_to_file(email_output, 'email')
        outputs['email'] = email_output
        file_paths['email'] = file_path

    if checkboxes.get('checkbox10', False):
        ssl_output = run_ssl(domain)
        file_path = save_output_to_file(ssl_output, 'ssl')
        outputs['ssl'] = ssl_output
        file_paths['ssl'] = file_path

    if checkboxes.get('checkbox11', False):
        tls_output = run_tls(domain)
        file_path = save_output_to_file(tls_output, 'tls')
        outputs['tls'] = tls_output
        file_paths['tls'] = file_path

    if checkboxes.get('checkbox12', False):
        port_output = run_port(domain)
        file_path = save_output_to_file(port_output, 'port')
        outputs['port'] = port_output
        file_paths['port'] = file_path

    if checkboxes.get('checkbox13', False):
        hping_output = run_hping(domain)
        file_path = save_output_to_file(hping_output, 'hping')
        outputs['hping'] = hping_output
        file_paths['hping'] = file_path

    return outputs, file_paths

def run_host(domain):
    safe_domain = shlex.quote(domain)
    try:
        host_result = subprocess.run(['python3', 'scripts/host.py', safe_domain], capture_output=True, text=True, check=True) 
        return host_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Host command failed: {e}")
        return "Host command failed."

def run_ws_office(domain):    
    safe_domain = shlex.quote(domain)
    try:
        ws_office_result = subprocess.run(['python3', 'scripts/ws_office.py', '-d', safe_domain], capture_output=True, text=True, check=True)
        return ws_office_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Workspace, Office 365 check script failed: {e}")  
        return "Workspace, Office 365 script failed."
    
def run_whois(domain):    
    safe_domain = shlex.quote(domain)
    try:
        whois_result = subprocess.run(['python3', 'scripts/who_is.py', safe_domain], capture_output=True, text=True, check=True)  
        return whois_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Whois script failed: {e}")  
        return "Whois script failed."

def run_subscraper(domain):
    safe_domain = shlex.quote(domain)
    try:
        subscraper_result = subprocess.run(['python3', 'scripts/subscraper.py' , '-d', safe_domain, '--resolve', '--cname'], capture_output=True, text=True, check=True)  
        return subscraper_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"subscraper script failed: {e}")  
        return "subscraper script failed."

def run_wafw00f(domain):
    safe_domain = shlex.quote(domain)
    try:
        result = subprocess.run(['wafw00f', safe_domain], capture_output=True, text=True, check=True) 
        output = result.stdout

        waf_detected_pattern = re.compile(r'is behind(.*?)\n')  # A regular expression pattern to detect the WAF name
        waf_search = waf_detected_pattern.search(output)  # Search for WAF name using the regular expression pattern

        if 'No WAF detected' in output:
            return 'No WAF detected on the domain: ' + safe_domain
        elif waf_search:
            # Extract and print the name of the WAF if detected
            waf_name = waf_search.group(1).strip()
            waf_name = remove_ansi_escape_sequences(waf_name)
            return 'WAF detected for ' + safe_domain + ': ' + waf_name
        else:
            return 'WAF status could not be determined for domain: ' + safe_domain

    except subprocess.CalledProcessError as e:
        return 'An error occurred while trying to run wafw00f: ' + str(e)

def run_shcheck(domain):
    safe_domain = shlex.quote(domain)
    try:
        shcheck_result = subprocess.run(['python3', 'scripts/shcheck.py', 'https://' + safe_domain], capture_output=True, text=True, check=True) 
        return shcheck_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"shcheck script failed: {e}")  
        return "shcheck script failed."
    
def run_wpscan(domain):
    safe_domain = shlex.quote(domain)
    try:
        wpscan_result = subprocess.run(['wpscan', '--url', 'https://www.' + safe_domain, '--no-banner', '-f', 'cli-no-colour'], capture_output=True, text=True, check=True) 
        return wpscan_result.stdout

    except subprocess.CalledProcessError as e:
        logging.error(f"wpscan failed: {e}") 
        return "No WordPress detected!"

def run_username(domainorg, page):
    safe_domain = shlex.quote(domainorg)
    try:
        username_result = subprocess.run(['python3', 'scripts/username.py' , '-d', '"' + safe_domain + '"', '-p', str(page), '-hl'], capture_output=True, text=True, check=True)
        return username_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Username script failed: {e}")  
        return "Username script failed."
    
def run_email(domain):
    safe_domain = shlex.quote(domain)
    try:
        email_result = subprocess.run(['python3', 'scripts/mail.py' , '-d', safe_domain], capture_output=True, text=True, check=True) 
        return email_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"email script failed: {e}") 
        return "email script failed."

def run_ssl(domain):
    safe_domain = shlex.quote(domain)
    try:
        ssl_result = subprocess.run(['python3' ,'scripts/ssl_checker.py' , '-d', safe_domain], capture_output=True, text=True, check=True) 
        return ssl_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"ssl script failed: {e}") 
        return "ssl script failed."
    
def run_tls(domain):
    safe_domain = shlex.quote(domain)
    try:
        tls_result = subprocess.run(['python3', 'scripts/tls.py', '-d', safe_domain], capture_output=True, text=True, check=True) 
        return tls_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"tlscheck script failed: {e}") 
        return "tlscheck script failed."

def run_port(domain):
    safe_domain = shlex.quote(domain)
    try:
        port_result = subprocess.run(['python3', 'scripts/port.py', safe_domain], capture_output=True, text=True, check=True) 
        return port_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"portcheck script failed: {e}")  
        return "portcheck script failed."

def run_hping(domain):    
    safe_domain = shlex.quote(domain)
    try:
        port_result = subprocess.run(['python3', 'scripts/hping.py', '-d',safe_domain], capture_output=True, text=True, check=True) 
        return port_result.stdout
    
    except subprocess.CalledProcessError as e:
        logging.error(f"hpingcheck script failed: {e}")  
        return "hpingcheck script failed."


#=====================================================================================================================================#
## These are short codes to sum up all the short code that us necessary ##

def remove_ansi_escape_sequences(text):
    ansi_escape_pattern = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape_pattern.sub('', text)

def generate_directory():
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex[:14]
    directory = os.path.join('/tmp', session['session_id'])
    os.makedirs(directory, exist_ok=True)
    return directory

def generate_unique_filename():
    unique_hex = uuid.uuid4().hex[:6]
    return f"osint_{unique_hex}.txt"

def save_output_to_file(output_content, check_name):
    directory = generate_directory()
    filename = generate_unique_filename()
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        file.write(output_content)
    return filepath

def compile_results_to_csv():
    directory = generate_directory()
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    combined_csv_path = os.path.join(directory, 'combined_results.csv')
    with open(combined_csv_path, 'w') as outfile:
        for file_path in all_files:
            with open(file_path) as infile:
                content = remove_ansi_escape_sequences(infile.read())
                outfile.write(content + "\n" + '================================================================================================================================' + '\n')
    return combined_csv_path

@app.route('/delete_files', methods=['POST'])
def delete_files():
    directory = os.path.join('/tmp', session.get('session_id', ''))
    try:
        shutil.rmtree(directory)
        return jsonify(success=True)  # Make sure this is sent back
    except Exception as e:
        return jsonify(success=False, error=str(e))


#=====================================================================================================================================#
@app.route('/download/<path:filename>')
def download(filename):
    directory = generate_directory()
    app.logger.debug(f"Attempting to send file '{filename}' from directory '{directory}'")
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

@app.route('/download_results')
def download_results():
    combined_csv_path = compile_results_to_csv()
    directory = os.path.dirname(combined_csv_path)
    filename = os.path.basename(combined_csv_path)
    return send_from_directory(directory=directory, path=filename, as_attachment=True)

@app.route('/')
def home():
    return render_template('readme.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/scanner')
def scanner():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=False)  # Start the Flask application with debugging turned off or on