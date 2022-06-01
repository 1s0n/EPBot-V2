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

parameters = dh.generate_parameters(generator=2, key_size=2048)
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

public_pem = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

iv = None
cipher = None
encryptor = None

def encrypt(msg):
    global iv, cipher, encryptor
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(msg) + encryptor.finalize()
    return ct

def sendenc(conn, msg, key):
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=msg,
    ).derive(key)
    conn.sendall(derived_key)

def decrypt(msg, key):


def HandleReq(conn, addr):
    header = conn.recv(1024).decode()
    header.replace("\r", "")
    headers = header.split("\n")
    reqDat = headers[0].split(" ")

    if reqDat[0] == "GET":
        conn.sendall(b"HTTP/1.1 400 Bad Request")
        conn.close()

    elif reqDat[0] == "CLIENT":
        print("Beginning encryption handshake...")
        
        conn.sendall(public_pem)

        print("Reciving public pem...")
        pemdat = conn.recv(1024)
        clientPubic = serialization.load_pem_private_key(pemdat)
        shared_key = server_private_key.exchange(serverPublic)
        print("Shared Key recived!")
        print("Verifying shared key...")
        sendenc(conn, secrets.token_hex(16), shared_key)

        print("Handshake complete!")
        
        
s.listen()

while True:
    c, a = s.accept()
    t = threading.Thread(target=HandleReq, args=(c, a,))
    t.start()