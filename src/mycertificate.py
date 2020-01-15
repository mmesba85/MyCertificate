#!/usr/bin/env python3

import argparse
import sys
import yaml
import gen
import check

parser = argparse.ArgumentParser()
parser.add_argument("-gen", type=str,
        help="For generation",
        choices=["CRT", "CSR", "KEY", "CA"],
        default=False)
parser.add_argument("-check", type=str,
        help="For cheking",
        choices=["CRT", "CSR", "KEY", "CA"],
        default=False)
parser.add_argument("-file", type=str,
        help="File to be checked",
        default=False)
parser.add_argument("-conf", type=str,
        help="Configuration file containing the name of the subject of the request",
        default=False)
parser.add_argument("-digest", type=str,
        help="Digestion method to use for signing",
        default="sha256")
parser.add_argument("-ktype", type=str,
        help="Type of the public key",
        default="RSA",
        choices=['RSA', 'DSA'])
parser.add_argument("-bits", type=int,
        help="Number of bits to encode the key",
        default=1024)
parser.add_argument("-serial", type=int,
        help="The serial number assigned to the certificate, default is random")
parser.add_argument("-expr", type=int,
        help="Expiration date of the certificate in years",
        default=10)
parser.add_argument("-pkey", type=str,
        help="File containing the public key",
        required=False)
parser.add_argument("-okey", type=str,
        help="Output file for the public key",
        required=False)
parser.add_argument("-ocrt", type=str,
        help="Output file for the self signed generated certificate",
        required=False)



args = parser.parse_args()
if args.gen:
    if args.gen == 'KEY':
        gen.generate_key(args.ktype, args.bits)
        exit(0)
    if args.serial is None:
        args.serial = -1
    f = args.conf
    
    name = {}
    try:
        with open(f, 'r') as file:
            name = yaml.safe_load(file)

    except Exception as e:
        print('Error while reading Configuration File. Configuration File must be in Yaml form.')
        print(e)

    if args.gen == 'CRT':
        gen.create_selfsigned_crt(args.pkey, args.ktype,
            args.bits, name, args.okey, 
            args.ocrt, args.digest, args.expr,
            args.serial)
    
    elif args.gen == 'CSR':
        gen.create_csr(args.pkey, name, args.digest, 
                        args.ktype, args.bits)

    elif args.gen == 'CA':
        gen.create_ca(args.ktype,
            args.bits, name, args.okey, 
            args.ocrt, args.digest, args.expr,
            args.serial)

elif args.check and args.file:
    if args.check == 'CRT':
        check.check_crt(args.file)
    elif args.check == 'CSR':
        check.check_csr(args.file)
    elif args.check == 'KEY':
        check.check_key(args.file)



