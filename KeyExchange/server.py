import socket
import rsa

s = socket.socket()

s.bind("127.0.0.1", 3214)

s.listen(0)

while True:
    conn, addr = s.accept()
    
