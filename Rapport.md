
# MyCertificate

Projet pour le cours Cyptologie Appliquée.

| Authors        | email                         |
| -------------- | ----------------------------- |
| Maroua Mesbahi | maroua.mesbahi@epita.fr       |
| Melissa Li     | melissa.li@epita.fr           |

Lien du github : https://github.com/mmesba85/MyCertificate

## Introduction

Nous avons choisi comme projet d'implémenter un gestionnaire de certificats.

### Qu'est ce qu'un certificat ?

Un certificat SSL est un fichier de données qui lie une clé cryptographique aux informations d'une organisation ou d'un individu.
SSL est un protocole utilisé pour sécuriser les échanges électroniques. Il permet de créer un dialogue de confiance entre un émetteur et un récepteur (par exemple un serveur web et un navigateur internet) en garantissant la légitimité de l’émetteur et en chiffrant toutes les données transmises

Ces certificats sont des fichiers créés pour établir une connexion sécurisée entre un serveur et un client (un émetteur et un récepteur)

#### Certificate signing request
Un CSR (Certificate Signing Request) est un message envoyé à partir d'un demandeur à une autorité de certification afin de demander un certificat d'identité numérique.

Avant de créer un CSR, le requérant crée une paire de clés (une publique et une privée) en gardant la clé privée secrète.

Le CSR contient des informations d'identification du demandeur, et la clé publique choisie par le demandeur.

La clé privée correspondante n'est pas incluse dans le CSR, mais est utilisée pour signer numériquement la demande. Le CSR peut être accompagné d'autres informations d'identification ou des preuves d'identité requises par l'autorité de certification, et l'autorité de certification peut contacter le demandeur pour plus d'informations.

Voici les informations typiquement présentes dans un CSR :

| Code | Information              |                                                                  |
|------|--------------------------| --- |
| C    | Country name             | Le code à deux lettres ISO pour le pays où est situé l'organisme |
| ST   | State or province name   | Par exemple Normandie, Ile-de-France                             |
| L    | Locality name            | Par exemple Paris, Londres                                       |
| O    | Organization name        | Nom d'une société ou d'une association légalement constituée     |
| OU   | Organizational unit name | Par exemple RH, finance, informatique                            |
| CN   | Common name              | Le nom complet du domaine Internet à sécuriser par exemple       |

La génération d’une demande de signature de certificat suppose de respecter quelques conventions, notamment :

- Créer une clé privée d’une longueur de 2048 bits (clé de type RSA 2018 Bits).
- S’assurer de la sécurité de la clé privée (en utilisant un outil de génération de clé suffisamment récent pour ne pas être vulnérable, et en définissant un mot de passe/une liste de contrôle pour en protéger l’accès).
- Utiliser un algorithme de signature en SHA256 (SHA 256withRSA) pour la CSR.

#### Génération de Certificat 
Le certificat est généré à l'aide du CSR généré précédement.

Le standard le plus utilisé pour la création des certificats numériques est le X.509

Un certificat électronique est un ensemble de données contenant :
- au moins une clé publique ;
- des informations d'identification, par exemple : nom, localisation, adresse électronique ;
- au moins une signature (construite à partir de la clé privée) ; de fait quand il n'y en a qu'une, l'entité signataire est la seule autorité permettant de prêter confiance (ou non) à l'exactitude des informations du certificat.

Les certificats électroniques et leur cycle de vie peuvent être gérés au sein d'infrastructures à clés publiques.

Les certificats électroniques respectent des standards spécifiant leur contenu de façon rigoureuse. Les deux formats les plus utilisés aujourd'hui sont :

- X.509, défini dans la RFC 52804
- OpenPGP, défini dans la RFC 48805

## Fonctionnement de l'outil

Notre outil est un gestionnaire de certificats. Codé en python, il est constitué de plusieurs modules:

gen.py : Génère, construit les clés, CSR et certificats
check.py : Vérifie les clés, CSR et certificats
mycertificate.py : Main

Nous générons des  certificat x509.

### Outils utilisés

Nous avons utilisé la bibliothèque pyopenssl pour la génération des clés, CSR et certificats.

Afin de générarer un certificat, les informations concernant l'autorité seront données dans un fichier de configuration de format YAML
##### exemple
```
C: FR
ST: Val-De-Marne
L: Kremlin-Bicetre
O: Certificate&co        
OU: titi
CN: toto
emailAddress: titi@mail.com
```
### Usage
```
$ python3 mycertificate.py -h
usage: mycertificate.py [-h] [-gen {CRT,CSR,KEY}] [-check {CRT,CSR,KEY}]
                        [-file FILE] [-conf CONF] [-digest DIGEST]
                        [-ktype {RSA,DSA}] [-bits BITS] [-serial SERIAL]
                        [-expr EXPR] [-pkey PKEY] [-okey OKEY] [-ocrt OCRT]

optional arguments:
  -h, --help            show this help message and exit
  -gen {CRT,CSR,KEY}    For generation
  -check {CRT,CSR,KEY}  For cheking
  -file FILE            File to be checked
  -conf CONF            Configuration file containing the name of the subject
                        of the request
  -digest DIGEST        Digestion method to use for signing
  -ktype {RSA,DSA}      Type of the public key
  -bits BITS            Number of bits to encode the key
  -serial SERIAL        The serial number assigned to the certificate, default
                        is random
  -expr EXPR            Expiration date of the certificate in years
  -pkey PKEY            File containing the public key
  -okey OKEY            Output file for the public key
  -ocrt OCRT            Output file for the self signed generated certificate
```

### Exemple d'utilisation
- Key generation:
```
maroua@maroua-XPS-13:~/Documents/Projets/MyCertificate/src$ python3 mycertificate.py -gen KEY -ktype DSA -bits 2048
maroua@maroua-XPS-13:~/Documents/Projets/MyCertificate/src$ cat file.key
-----BEGIN PRIVATE KEY-----
MIICZQIBADCCAjkGByqGSM44BAEwggIsAoIBAQCPo3EjOmvASIaO7KuQGNOVPz9r
yLnPhebBSoikhEY9JOov1ssLe9vIjgrZPwfDLxusLePNHHoADpCxmlQEilpyM1dE
XNTC0y2g1ITjcM4twMKyZHsYqleabw+BcjX5Yjf/Xs/5J7NOmfMcvFhJrRe98DvS
EdZ1BRX85p8Pe1TYvzK03T6jjd402kt16qGL053SkfbBWHJGW3IB202NI5liMwZ5
JS9nh7YlBpw5bfE9CkohFcJSoy6Iis+B/AoRjP6QPXYFBsyuELfqQo37RFRWSpMB
RsOyuaKIBJQptat2QJauH92F1FnqotTmcoukQ2r5lAlszHz30s0s+fmSMmDHAiEA
9TeM1MT7vDMkISlFvtZ+u2rRHYdZuIJVFSnojJ3fYFUCggEAICbZ/VgyNhO57fu/
atAtxMpO2Wbgjn1gYjCQtRw0rpCOWcjOtMndz2URxKgdPr1PCzjYsDz8BceSCvOP
gcIZzXfc1aHjJASPB8nB9xKAlMzdEmorA0btrZR807gotFZlUPQlEkZzIDfEPo+z
iqF6fMk4Nmowe0qwZ63GmeIxcb0Tn/t8c1HZlr/ANibTPuiLqoHpsPZlHydIcMoc
VWsKKj/516DOeWnXfBLEepX3ie6dcXvq09jN2phVWMidZXDJtJ147JpgS4P1EiQJ
vlwGIOD7HZYa2DVAfh3FU5qmFpfx3NoLHfZ5WW4EQHyu4f1LvVDXD3bfuGFWC9pu
mTtXggQjAiEAviHYzNFHdpfZckpNGTowylOXLwd1gSgAGJD8Qw0yMvI=
-----END PRIVATE KEY-----
```
- CSR generation:
```
maroua@maroua-XPS-13:~/Documents/Projets/MyCertificate/src$ python3 mycertificate.py -gen CSR -conf conf.yaml -ktype RSA -bits 1024 
maroua@maroua-XPS-13:~/Documents/Projets/MyCertificate/src$ cat file.csr
-----BEGIN CERTIFICATE REQUEST-----
MIIB1DCCAT0CAQAwgZMxCzAJBgNVBAYTAkZSMRUwEwYDVQQIDAxWYWwtRGUtTWFy
bmUxGDAWBgNVBAcMD0tyZW1saW4tQmljZXRyZTEXMBUGA1UECgwOQ2VydGlmaWNh
dGUmY28xDTALBgNVBAsMBHRpdGkxDTALBgNVBAMMBHRvdG8xHDAaBgkqhkiG9w0B
CQEWDXRpdGlAbWFpbC5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAOvk
xfL4nV3LNlyE58EsRmIKYZGCS2ThX8b/ja0OsVlkS0yHP46tF0pvUj3Xw55wjw3m
GqPhWcIofGOMVZGIwpEwRrFlN6PM+wp1sv6W+JQPzwTlpTlP3GIAamhGMrkVWwhF
HBdIxUJdHh2RA/1TgancQK7Zcy7xKts1ochlkXUJAgMBAAGgADANBgkqhkiG9w0B
AQsFAAOBgQCcoJ9S0zgyDbRwyshFriAMJjlqwTz+ck0fUUWy1gqfMwGzgJfmJ5L2
84RbZUsneNG5xj+eqNLICDUg/a15lHmjtV2NUtuyA0dndYsdaS56RRsHrYs4AJn+
M+9XLkOaA9WgJldBstQzX6U9zxW4gg4w3p38/BRbPPkHRvdTktMFkA==
-----END CERTIFICATE REQUEST-----
```
- Check CSR:
```
maroua@maroua-XPS-13:~/Documents/Projets/MyCertificate/src$ python3 mycertificate.py -check CSR -file file.csr
Certificate Request:
Common name: toto
Organisation: Certificate&co
Orgainistional unit: titi
City/locality: Kremlin-Bicetre
State/province: Val-De-Marne
Country: FR
Signature algorithm: 
Key algorithm: RSA
Key size: 1024
Version: 0
```
## Difficultés rencontrées

Nous avons pris beaucoup de temps au début du projet pour la compréhension des différentes fonctions du package pyopenssl.

## Améliorations possibles

Conversion du certificat au format DER/PEM.
Déploiement du certificat.
