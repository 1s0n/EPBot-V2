import secrets
import socket
import rsa

print("Generating new encryption keys...")

public_key, private_key = rsa.newkeys(2048)

print("Getting pem of public key...")
public_pem = public_key.save_pkcs1('PEM')

s = socket.socket()

s.bind(("127.0.0.1", 3214))

s.listen()

while True:
    conn, addr = s.accept()
    print("Connection from port " + str(addr[1]))
    conn.sendall(public_pem)

    keyEnc = conn.recv(256)

    key = rsa.decrypt(keyEnc, private_key)

    print("Confirming handshake hash with backup server...")

    sec = secrets.token_bytes()

    vers = socket.socket()
    s.connect(("127.0.0.1", 9821))
    s.sendall(b"1")
    b.sendall()