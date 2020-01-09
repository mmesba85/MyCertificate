#!/usr/bin/env python

from OpenSSL import crypto, SSL
import subprocess, os, sys
import random

KEY_FILE = 'file.key'
CSR_FILE = 'file.csr'
CERT_FILE = 'file.crt'

"""
Generate a public key

Arguments:  type - key type
            bits - number of bits

Returns:    generated public key
"""
def generate_key(type, bits):
    key = crypto.PKey()
    key.generate_key(type, bits)
    f = open(KEY_FILE, "w")
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    f.close()
    return key

"""
Load key from file

Arguments:  filename - file containing the public key

Returns:    public key
"""
def load_key(filename):
    key = open(filename)
    res = crypto.load_privatekey(crypto.FILETYPE_PEM, key.read())
    return res

"""
Create a certificate request.
 
Arguments:  pkey   - The key to associate with the request
            **name - The name of the subject of the request
                          C     - Country name
                          ST    - State or province name
                          L     - Locality name
                          O     - Organization name
                          OU    - Organizational unit name
                          CN    - Common name
                          emailAddress - E-mail address
            digest - Digestion method to use for signing, default is sha256
Returns:   The certificate request
"""
def create_csr(pkey, name,  digest="sha256"):
    
    req = crypto.X509Req()
    subj = req.get_subject()
 
    for key, value in name.items():
        setattr(subj, key, value)
 
    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    f = open(CSR_FILE, "w")
    f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
    f.close()

    return req

"""
Create a certificate request.
 
Arguments:  pkey   - The key to associate with the request
            **name - The name of the subject of the request
            digest - Digestion method to use for signing, default is sha256
            key_file - File to store the public key, default is KEY_FILE
            cert_file - File to store the certificate, default is CERT_FILE
            exprdate - Expiration date in years, default is 10
            serial_number - The serial number assigned to the certificate, 
                default is random

Returns:   The self signed certificate
"""
def create_selfsigned_cert(type_, bits, name,  digest="sha256",
                               key_file=KEY_FILE, cert_file=CERT_FILE,
                               exprdate=10, serial_number=-1):
   k = generate_key(type_, bits)
   cert = crypto.X509()
   subj = cert.get_subject()
  
   for key, value in name.items():
       setattr(subj, key, value)
 
   if serial_number == -1:
       serial_number=random.getrandbits(64)
 
   cert.set_serial_number(serial_number)
   cert.gmtime_adj_notBefore(0)
   cert.gmtime_adj_notAfter(exprdate*365*24*60*60)
   cert.set_issuer(cert.get_subject())
   cert.set_pubkey(k)
   cert.sign(k, digest)
   open(cert_file, 'wt').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
   open(key_file, 'wt').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


res = generate_key(crypto.TYPE_RSA, 1024)

name = {'C' : 'FR', 
        'ST' : 'Val-De-Marne', 
        'L' : 'Maisons-Alfort',
        'O' : 'MarouaCo',
        'OU' : 'titi',
        'CN' : 'toto',
        'emailAddress' : 'titi@mail.com'}
req = create_csr(res, name)
print(req)

t = create_selfsigned_cert(crypto.TYPE_RSA, 1024, name)
