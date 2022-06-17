from hashlib import md5, sha256
import socket
from time import sleep 
import rsa
import secrets

from cryptography.fernet import Fernet

print("Connecting to server...")
s = socket.socket()

s.connect(("127.0.0.1", 3214))

print("Starting handshake...")
public_pem = s.recv(1024)

public_key = rsa.PublicKey.load_pkcs1(public_pem)

print("Server public key recived, generating encryption key...")
key = Fernet.generate_key()

fernet = Fernet(key)

keyEnc = rsa.encrypt(key, public_key)

s.sendall(keyEnc)

sec = s.recv(1024)
server_secret = fernet.decrypt(sec)

verhash = server_secret + key
print(verhash)
verhash = md5(verhash).hexdigest().encode()
print(verhash)
while s.recv(4) == "":
    print("A")
    sleep(0.1)
sleep(2)
vers = socket.socket()
vers.connect(("127.0.0.1", 9821))
vers.sendall(b"2")
vers.sendall(verhash)
resp = vers.recv(6)
vers.close()
if resp == b"ACCEPT":
    print("Handshake data confirmed!")
    print("Handshake complete!")
else:
    print("Handshake hash verification failed!")
    print("Handshake failed! Closing connection...")
    s.close()

s.close()