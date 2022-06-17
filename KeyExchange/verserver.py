import socket
import threading
import time

s = socket.socket

s.bind(("127.0.0.1", 9821))

s.listen()

awaiting_confirmation = []

# Verification hash structure: secret + client encryption key

def handle(conn, addr):
    print("Request from " + addr)
    if addr[0] == "127.0.0.1":
        d = conn.recv(1)
        if d == b"1":    
            print("Request from server!")
            dat = conn.recv(1024)
            awaiting_confirmation.append(dat)
            timer = 5000
            while timer > 0:
                timer -= 1
                try:
                    awaiting_confirmation[dat]
                except KeyError:
                    conn.send(b"ACCEPT")
                    break
            
            conn.send(b"FAILED")
            return
    
    dat = conn.recv(1024)
    try:
        awaiting_confirmation.remove(dat)
    except:
        conn.send(b"FAILED")


def handleReq(conn, addr):
    try:
        handle(conn, addr)
    except:
        conn.close()

while True:
    conn, addr = s.accept()
    t = threading.Thread(target=handleReq, args=(conn, addr,))
    t.start()