import socket

s = socket.socket()
s.bind("127.0.0.1", 4321)

pending_requests = {}

def handleReq(conn, addr):
    ip = addr[0]

    if ip == "127.0.0.1":
        print("Server verification request!")
        serverdata = conn.recv(1024)
        