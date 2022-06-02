import threading
import socket

s = socket.socket()

s.bind(("127.0.0.1", 1234))

s.listen()

httpResponse = """
HTTP/1.1 200 OK
Content-Type: {ContentType}; charset={Charset}
Date: Tue, 31 May 2022 05:34:01 GMT
Server: VeryCoolServer
Connection: close
{ExtraHeaders}

{Content}
"""

def index():
    return httpResponse.format(ContentType="text/html", Charset="UTF-8", ExtraHeaders="", Content="<b>IT WORKS</b>").encode()

urls = {
    "/": index
}

def httpReq(conn, addr):
    header = conn.recv(1024).decode()
    header.replace("\r", "")
    headers = header.split("\n")
    reqDat = headers[0].split(" ")

    if reqDat[0] == "GET":
        path = reqDat[1]

        if path in urls:
            conn.sendall(urls[path]())


while True:
    try:
        a, b = s.accept()
        t = threading.Thread(target=httpReq, args=(a, b,))
        t.start()

    except KeyboardInterrupt:
        print("A")
        s.close()
        break
