import socket
from OpenSSL import SSL
from argparse import ArgumentParser
from datetime import datetime

class SSLChecker:
    def get_cert(self, host, port):
        # Connection to the host.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        osobj = SSL.Context(SSL.TLSv1_2_METHOD)
        sock.connect((host, int(port)))
        oscon = SSL.Connection(osobj, sock)
        oscon.set_tlsext_host_name(host.encode())
        oscon.set_connect_state()
        oscon.do_handshake()
        cert = oscon.get_peer_certificate()
        resolved_ip = socket.gethostbyname(host)
        sock.close()
        return cert, resolved_ip

    def get_cert_sans(self, x509cert):
        # Get Subject Alt Names from Certificate.
        san = ''
        ext_count = x509cert.get_extension_count()
        for i in range(ext_count):
            ext = x509cert.get_extension(i)
            if 'subjectAltName' in str(ext.get_short_name()):
                san = ext.__str__()
        return san.split(', ')

    def get_cert_info(self, host, cert, resolved_ip):
        # Get all the information about cert.
        cert_subject = cert.get_subject()
        cert_issuer = cert.get_issuer()
        valid_from = datetime.strptime(cert.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        valid_till = datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        now = datetime.now()
        days = (valid_till - now).days
        return {
            'host': host,
            'server_IP': resolved_ip,
            'issued_domain': cert_subject.CN,
            'issued_to': cert_subject.O,
            'issued_by': cert_issuer.organizationName+' '+'('+cert_issuer.countryName+')',
            'valid_from': valid_from.strftime('%Y-%m-%d'),
            'valid_till': valid_till.strftime('%Y-%m-%d')+' '+'('+ str(days)+' days left)',
            'validity_days': (valid_till - valid_from).days,
            'cert_valid': not cert.has_expired(),
            'cert_s/n': str(cert.get_serial_number()),
            'cert_sha1': cert.digest('sha1').decode(),
            'cert_version': cert.get_version(),
            'cert_algorithm': cert.get_signature_algorithm().decode(),
            'expired': cert.has_expired(),
            'cert_sans': self.get_cert_sans(cert)
        }

    def print_status(self, info):
        # Print all the useful info about host.
        check_mark = '✓' if info['cert_valid'] else '✗'
        print('[{}] {}\n'.format(check_mark, info['host']))
        for key, value in info.items():
            if key not in ['host']:
                if key == 'cert_sans':
                    print('Certificate SANs:')
                    for san in value:
                        print('  - {}'.format(san))
                else:
                    print('{}: {}'.format(' '.join(key.capitalize().split('_')), value))

    def run(self, hosts):
        # Run the checker.
        for host in hosts:
            host, port = self.filter_hostname(host)
            try:
                cert, resolved_ip = self.get_cert(host, port)
                info = self.get_cert_info(host, cert, resolved_ip)
                self.print_status(info)
            except Exception as e:
                print('Failed to get certificate for {}: \n\n{}'.format(host, e))

    def filter_hostname(self, host):
        # Remove unused characters and split by address and port.
        host = host.replace('http://', '').replace('https://', '').replace('/', '')
        return host, 443

    def get_args(self):
        # Set argparse options.
        parser = ArgumentParser(description="Collects useful information about the given host's SSL certificates.")
        parser.add_argument('-d', '--domain', dest='domain', nargs='+', required=True, help=' as input separated by space')
        return parser.parse_args()

if __name__ == '__main__':
    ssl_checker = SSLChecker()
    args = ssl_checker.get_args()
    ssl_checker.run(args.domain)