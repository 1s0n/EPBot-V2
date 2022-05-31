import threading
import socket

s = socket.socket()

s.bind(("127.0.0.1", 1233))

s.listen()

def index():
    return ""

urls = {
    "/": index
}

def httpReq(conn, addr):
    header = conn.recv(1024).decode()
    header.split("\r", "")
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
        t.daemon = True
        t.start()

    except KeyboardInterrupt:
        print("A")
        s.close()
        break


"""
GET / HTTP/1.1
Host: 127.0.0.1:1233
Connection: keep-alive
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
DNT: 1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5
"""