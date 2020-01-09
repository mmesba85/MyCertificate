#!/usr/bin/env python

import argparse
import sys
import yaml
import gen

parser = argparse.ArgumentParser()
parser.add_argument("-gen", type=str,
        help="For generation",
        choices=["CRT", "CSR"],
        default=False)
parser.add_argument("-conf", type=str,
        help="Configuration file containing the name of the subject of the request",
        default=False,
        required='-gen' in sys.argv)
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
print(args)
if args.gen:
    if args.serial is None:
        args.serial = -1
    f = args.conf
    with open(f, 'r') as file:
        name = yaml.load(file, Loader=yaml.FullLoader)

    if args.gen == 'CRT':
        gen.create_selfsigned_crt(args.ktype,
            args.bits, name, args.okey, 
            args.ocrt, args.digest, args.expr,
            args.serial)
    
    elif args.gen == 'CSR':
        gen.create_csr(args.pkey, name, args.digest, 
                        args.ktype, args.bits)


