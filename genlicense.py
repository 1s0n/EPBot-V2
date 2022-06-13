from random import choice
import sqlite3

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

"""
s = socket.socket()
s.connect(("127.0.0.1", 1234)) # Going to be 9090 when deployed as it is the port the server is pointed at
"""

def genKey():
    s = []
    for i in range(32):
        s.append(choice(chars))
    return "".join(s)

def addKey(key):
    con = sqlite3.connect('license.db')
    cur = con.cursor()
    cur.execute("INSERT INTO token (data) VALUES (?);", (key,))
    con.commit()
    con.close()


"""
CREATE TABLE token (
ind INTEGER PRIMARY KEY,
data TEXT NOT NULL
);
"""

"""
CREATE TABLE emails (
ind INTEGER PRIMARY KEY,
email TEXT NOT NULL
);
"""

if __name__ == "__main__":
    k = genKey()
    addKey(k)