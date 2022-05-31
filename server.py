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
        
s.listen()

while True:
    c, a = s.accept()
    t = threading.Thread(target=HandleReq, args=(c, a,))
    t.start()