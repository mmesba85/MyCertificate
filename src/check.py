from OpenSSL import crypto, SSL
from OpenSSL._util import exception_from_error_queue as _exception_from_error_queue


def print_subject(req):
    key = req.get_pubkey()
    key_type = 'RSA' if key.type() == crypto.TYPE_RSA else 'DSA'
    subject = req.get_subject()
    components = dict(subject.get_components())
    print "Common name:", components['CN']
    print "Organisation:", components['O']
    print "Orgainistional unit", components['OU']
    print "City/locality:", components['L']
    print "State/province:", components['ST']
    print "Country:", components['C']
    print "Signature algorithm:", '?'
    print "Key algorithm:", key_type
    print "Key size:", key.bits()
    print "Version: ", req.get_version()
    

def check_csr(file_name):
    f = open(file_name, "r")
    csr = f.read()
    try:
        req = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr)
        print_subject(req)
    except crypto.Error:
        print("Certificate Signing Request is inconsistent.")

def check_crt(file_name):
    f = open(file_name, "r")
    crt = f.read()
    try:
        req = crypto.load_certificate(crypto.FILETYPE_PEM, crt)
        print_subject(req)
        print "Has expired? ", req.has_expired()
        print(req.get_issuer)
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
