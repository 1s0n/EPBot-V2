from random import choice
import sqlite3

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

def genKey(len=32):
    s = []
    for i in range(len):
        s.append(choice(chars))
    return "".join(s)

def addKey(key, length):
    con = sqlite3.connect('license.db')
    cur = con.cursor()
    cur.execute("INSERT INTO tokens (data, length) VALUES (?, ?);", (key,length,))
    con.commit()
    con.close()


""" Restore database:

CREATE TABLE tokens (
ind INTEGER PRIMARY KEY,
data TEXT NOT NULL,
length INTEGER NOT NULL
);

CREATE TABLE users (
ind INTEGER PRIMARY KEY,
email TEXT NOT NULL,
password TEXT NOT NULL,
enckey TEXT NOT NULL,
enckey2 TEXT NOT NULL,
expirydate INTEGER NOT NULL,
token TEXT NOT NULL,
branch TEXT NOT NULL,
advanced_account INTEGER NOT NULL
);
"""

if __name__ == "__main__":
    k = genKey()
    print(k)
    leng = input("length the key will be active (days): ")
    leng = int(leng)
    input("Press control-c to cancel key creation...")
    addKey(k, leng)