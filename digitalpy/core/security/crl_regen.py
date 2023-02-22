from OpenSSL import crypto
import argparse

CA_PEM_PATH = "ca.pem"
CA_KEY_PATH = "ca.key"
CRL_FILE = "FTS_CRL.json"

class CertficateRevocationListController:
    def __init__(ca_pem_path: str, ca_key_path: str, crl_file_path: str):
        self.ca_pem_path = ca_pem_path
        self.ca_key_path = ca_key_path
        self.ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(CA_KEY_PATH).read())
        self.ca_pem = crypto.load_certificate(crypto.FILETYPE_PEM, open(CA_PEM_PATH, 'rb').read())
        self.crl_file_path = crl_file_path

    def regenerate_crl(self):
        """regenerate the configured crl"""

        # instantiate CRL object
        crl = crypto.CRL()
        crl.sign(self.ca_pem, self.ca_key, b"sha256")

        # open CRL file and write CRL contents
        with open(self.crl_file_path, 'wb') as f:
            f.write(crl.export(cert=self.ca_pem, key=self.ca_key, digest=b"sha256"))


        delete = 0
        # read the contents of the ca pem
        with open(self.ca_pem_path, "r") as f:
            lines = f.readlines()
        # re-write the contents of the ca pem until x509 crl is reached
        with open(self.ca_pem_path, "w") as f:
            for line in lines:
                if delete:
                    continue
                elif line.strip("\n") != "-----BEGIN X509 CRL-----":
                    f.write(line)
                else:
                    delete = 1
        
        # add the updated x509 crl to the end of the ca pem
        with open(self.ca_pem_path, "ab") as f:
            f.write(crl.export(cert=self.ca_pem, key=self.ca_key, digest=b"sha256"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='command line arguments')
    parser.add_argument('--ca-pem-path', dest='ca_pem_path', type=str, help='path to the certificate authority pem')
    parser.add_argument('--ca-key-path', dest='ca_key_path', type=str, help='path to the certificate authority key')
    parser.add_argument('--crl-path', dest='crl_path', type=str, help='Path to the CRL')

    args = parser.parse_args()
    
    CertficateRevocationListController(args.ca_pem_path, args.ca_key_path, args.crl_path).regenerate_crl()