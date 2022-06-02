print("Starting...")
import socket
import secrets
import threading
s = socket.socket()
s.bind(("127.0.0.1", 1234))

print("Setting up encryption stuff...")
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives import serialization
_parampem = b'-----BEGIN DH PARAMETERS-----\nMIIBCAKCAQEA0cCWPFextsxjaaOPT0HYHiTocc8nu/DRv3bSJjPPVUox94tVthlx\nDayDuJc4HdKAwqiOICKDEpSTBUsapDn/5R1heR7kVtL525+ioZeDkm2YusyfUW5q\nnLvPqXqecJ1Mx1WnE+PAne8ZAx9shcuiD4sIBhCAYHWaFVPDGak6QuIbGFLIekIa\nG6l8YwS2YfH+bkb8zPt0aOLwjgOolewLVUjD4ap94svYaPWvL8CyVQgmZYTpNCCL\n99fqBLKCKlW6wbGuY6FgcuoU6eCeL6yEUBd0cNUA4ehShVOdefUFSnGFM4KHIsCh\nK5+kI74v6MC3E6UfpjdiXZ0sL+3YxsodBwIBAg==\n-----END DH PARAMETERS-----\n'

# Parameters are not generated each time
parameters = serialization.load_pem_parameters(_parampem)

print("Loading license keys...")

licensedat = ""

with open("LicKey.json") as f:
    licensedat = f.read()
    f.close()

import json
licenses = json.loads(licensedat)

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt(msg, key):
    iv = None
    cipher = None
    encryptor = None
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(msg) + encryptor.finalize()
    del cipher
    del encryptor
    return ct

def sendenc(conn, msg, key):
    data = encrypt(msg, key)
    conn.sendall(data)

def decrypt(ct, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    msg = decryptor.update(ct) + decryptor.finalize()
    return msg

def HandleReq(conn, addr):
    print("Accepted!")
    header = conn.recv(1024).decode()
    header.replace("\r", "")
    headers = header.split("\n")
    reqDat = headers[0].split(" ")

    if reqDat[0] == "GET":
        conn.sendall(b"HTTP/1.1 400 Bad Request")
        conn.close()

    elif reqDat[0] == "CLIENT":
        print("Beginning encryption handshake...")
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
        conn.sendall(public_pem)

        print("Reciving public pem...")
        pemdat = conn.recv(1024)
        clientPubic = serialization.load_pem_public_key(pemdat)
        shared_key = private_key.exchange(clientPubic)
        print("Shared Key recived!")
        print("Verifying shared key...")
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'Handshake_Verification',
        ).derive(shared_key)
        key2 = conn.recv(len(derived_key))
        if key2 == derived_key:
            
            print("Handshake complete!")
        else:
            print("KEYERROR!")
            conn.close()
            return
    
    elif reqDat[0] == "ADMIN":
        print("New admin request!")
        if not addr[0] == "127.0.0.1":
            print("WARNING: ADMIN REQUEST NOT FROM LOCALHOST!")

        print("Beginning encryption handshake...")
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
        conn.sendall(public_pem)

        print("Reciving public pem...")
        pemdat = conn.recv(1024)
        clientPubic = serialization.load_pem_public_key(pemdat)
        shared_key = private_key.exchange(clientPubic)
        print("Shared Key recived!")
        print("Verifying shared key...")
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'Handshake_Verification',
        ).derive(shared_key)
        key2 = conn.recv(len(derived_key))
        if key2 == derived_key:
            
            print("Handshake complete!")
        else:
            print("KEYERROR!")
            conn.close()
            return
        
        data = conn.recv(1024)



print("Listening...")
        
s.listen()

while True:
    c, a = s.accept()
    t = threading.Thread(target=HandleReq, args=(c, a,))
    t.start()