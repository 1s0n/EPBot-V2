from random import choice
import sqlite3

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

def genKey():
    s = []
    for i in range(32):
        s.append(choice(chars))
    return "".join(s)

def addKey(key):
    con = sqlite3.connect('license.db')
    cur = con.cursor()
    cur.execute("INSERT INTO tokens (data) VALUES (?);", (key,))
    con.commit()
    con.close()


""" Restore database:

CREATE TABLE tokens (
ind INTEGER PRIMARY KEY,
data TEXT NOT NULL
);

CREATE TABLE users (
ind INTEGER PRIMARY KEY,
email TEXT NOT NULL,
password TEXT NOT NULL
);
"""

if __name__ == "__main__":
    k = genKey()
    print(k)
    input("Press control-c to cancel key creation...")
    addKey(k)