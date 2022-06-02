from random import choice
import jwt
import socket
import uuid
import sqlite3

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

"""
s = socket.socket()
s.connect(("127.0.0.1", 1234)) # Going to be 9090 when deployed as it is the port the server is pointed at
"""

def gensalt(l=16):
    s = []
    for i in range(l):
        s.append(choice(chars))
    return "".join(s)

keyid = input("Identifyer for key, salt added so it can be the same for multiple keys: ")
uid = str(uuid.uuid4())
salt = gensalt()
keyid = salt + keyid

secret = gensalt(l=32)

dictdat = {"id": keyid, "salt": salt, "uuid": uid}
encoded_jwt = jwt.encode(dictdat, secret, algorithm="HS256")


"""
CREATE TABLE token (
ind INTEGER PRIMARY KEY,
data TEXT NOT NULL
);
"""

"""
CREATE TABLE accHashes (
    ind INTEGER PRIMARY KEY,
    token TEXT NOT NULL
);
"""

con = sqlite3.connect('keys.db')
cur = con.cursor()
cur.execute("INSERT INTO token (data) VALUES (?);", (encoded_jwt,))
con.commit()
con.close()