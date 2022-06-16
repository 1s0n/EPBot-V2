import socket 
import rsa

s = socket.socket()

s.connect("127.0.0.1", 3214)

public_key, private_key = rsa.newkeys(2048)

public_pem = public_key.save_pkcs1('PEM')

