import json
from random import choice
import jwt
import socket
import uuid

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

s = socket.socket()
s.connect(("127.0.0.1", 1234)) # Going to be 9090 when deployed as it is the port the server is pointed at

def gensalt(l=16):
    s = []
    for i in range(l):
        s.append(choice(chars))
    return "".join(s)

keyid = input("Identifyer for key, salt added so it can be the same for multiple keys:")
uid = str(uuid.uuid4())
salt = gensalt()
keyid = salt + keyid

secret = gensalt(l=32)

dictdat = {"name": keyid, "salt": salt, "uuid": uid}
encoded_jwt = jwt.encode(dictdat, secret, algorithm="HS256")

jsondat = {"TOKEN": encoded_jwt, "SECRET": secret}

