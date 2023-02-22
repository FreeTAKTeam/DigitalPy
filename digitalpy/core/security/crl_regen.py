from OpenSSL import crypto

CA_PEM_PATH = "ca.pem"
CA_KEY_PATH = "ca.key"
CRL_FILE = "FTS_CRL.json"

ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(CA_KEY_PATH).read())
ca_pem = crypto.load_certificate(crypto.FILETYPE_PEM, open(CA_PEM_PATH, 'rb').read())
# append empty crl
crl = crypto.CRL()
crl.sign(ca_pem, ca_key, b"sha256")

with open(CRL_FILE, 'wb') as f:
    f.write(crl.export(cert=ca_pem, key=ca_key, digest=b"sha256"))

delete = 0
with open(CA_PEM_PATH, "r") as f:
    lines = f.readlines()
with open(CA_PEM_PATH, "w") as f:
    for line in lines:
        if delete:
            continue
        elif line.strip("\n") != "-----BEGIN X509 CRL-----":
            f.write(line)
        else:
            delete = 1

with open(CA_PEM_PATH, "ab") as f:
    f.write(crl.export(cert=ca_pem, key=ca_key, digest=b"sha256"))