import socket 
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

keyEnc = rsa.encrypt(key, public_key)
print(len(keyEnc))
s.sendall(keyEnc)

