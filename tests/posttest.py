import socket, json

s = socket.socket()
s.bind(("127.0.0.1", 1234))

s.listen(0)


while True:
    conn, addr = s.accept()
    print(addr)
    req = conn.recv(2048).decode()

    reqdat = req.split("\r\n\r\n")
    print(reqdat)
    
    conn.sendall(b"HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\r\n\r\n{\"test\":\"moretest\"}")
    conn.close()

    