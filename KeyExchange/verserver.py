import socket
import threading
import time

s = socket.socket()

s.bind(("127.0.0.1", 9821))

s.listen()

awaiting_confirmation = {}
print("Listening...")
# Verification hash structure: secret + client encryption key

def handle(conn, addr):
    global awaiting_confirmation
    print("Request from " + addr[0])
    if addr[0] == "127.0.0.1":
        d = conn.recv(1)
        if d == b"1":    
            print("Request from server!")
            dat = conn.recv(1024)
            awaiting_confirmation[dat] = 0
            print("added hash " + str(dat))
            timer = 5000
            while timer > 0:
                timer -= 1
                if awaiting_confirmation.get(dat) == None:
                    print("ACCEPT")
                    conn.send(b"ACCEPT")
                    break
                time.sleep(0.1)

            if timer <= 0:
                conn.send(b"FAILED")
            return
    
    dat = conn.recv(1024)
    print("Client hash " + str(dat))
    if not awaiting_confirmation.get(dat) == None:
        print("ACC")
        awaiting_confirmation.pop(dat)
        conn.send(b"ACCEPT")
    else:
        conn.send(b"FAILED")


def handleReq(conn, addr):
    try:
        handle(conn, addr)
    except KeyboardInterrupt as e:
        print(e)
    print("Closing conn")
    conn.close()

while True:
    conn, addr = s.accept()
    print("NewConn")
    t = threading.Thread(target=handleReq, args=(conn, addr,))
    t.start()