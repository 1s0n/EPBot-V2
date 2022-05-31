import socket

s = socket.socket()

s.bind(("127.0.0.1", 1234))

s.listen()

def httpReq(conn, addr):
