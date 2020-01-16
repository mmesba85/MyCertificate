from OpenSSL import crypto, SSL
from OpenSSL._util import exception_from_error_queue as _exception_from_error_queue


def print_subject(req):
    key = req.get_pubkey()
    key_type = 'RSA' if key.type() == crypto.TYPE_RSA else 'DSA'
    subject = req.get_subject()
    components = dict(subject.get_components())
    print("Common name: %s" % components.get(b'CN').decode())
    print("Organisation: %s" % components.get(b'O').decode())
    print("Orgainistional unit: %s" % components.get(b'OU').decode())
    print("City/locality: %s" % components.get(b'L').decode())
    print("State/province: %s" % components.get(b'ST').decode())
    print("Country: %s" % components.get(b'C').decode())
    print("Signature algorithm: ")
    print("Key algorithm: %s" % key_type)
    print("Key size: %s" % key.bits())
    print("Version: %s" % req.get_version())
    

def check_csr(file_name):
    f = open(file_name, "r")
    csr = f.read()
    try:
        req = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr)
        print("Certificate Request:")
        print_subject(req)
    except crypto.Error:
        print("Certificate Signing Request is inconsistent.")

def check_crt(file_name):
    f = open(file_name, "r")
    crt = f.read()
    try:
        req = crypto.load_certificate(crypto.FILETYPE_PEM, crt)
        print("Certificate:")
        print_subject(req)
        print("Has expired? %s" % req.has_expired())
        print("Serial Number: %s" % req.get_serial_number())
    except crypto.Error:
        print("Certificate is inconsistent.")

def check_key(file_name):
    f = open(file_name)
    key = f.read()
    try:
        res = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
        t = res.check()
        print("Key is consistent.")
    except crypto.Error:
        print("Key is inconsistent.")
    except TypeError:
        print("TypeError: key can't be checked.")
