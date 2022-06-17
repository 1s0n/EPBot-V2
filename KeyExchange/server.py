from hashlib import md5, sha256
import secrets
import socket
import rsa
from cryptography.fernet import Fernet

print("Generating new encryption keys...")

public_key, private_key = rsa.newkeys(2048)

print("Getting pem of public key...")
public_pem = public_key.save_pkcs1('PEM')

s = socket.socket()

s.bind(("127.0.0.1", 3214))

s.listen(1)

while True:
    conn, addr = s.accept()
    print("Connection from port " + str(addr[1]))
    conn.sendall(public_pem)

    keyEnc = conn.recv(256)

    key = rsa.decrypt(keyEnc, private_key)

    fernet = Fernet(key)

    sec = secrets.token_hex(32).encode()

    conn.sendall(fernet.encrypt(sec))

    print("Confirming handshake hash with backup server...")


    verhash = sec + key
    print(verhash)
    verhash = md5(verhash).hexdigest().encode() 
    print(verhash)
    vers = socket.socket()
    vers.connect(("127.0.0.1", 9821))
    vers.sendall(b"1")
    vers.sendall(verhash)
    conn.send(b"send")
    resp = vers.recv(6)
    vers.close()
    if resp == b"ACCEPT":
        print("Handshake data confirmed!")
        print("Handshake complete!")
    else:
        print("Handshake hash verification failed!")
        print("Handshake failed! Closing connection...")
        conn.close()
    conn.close()