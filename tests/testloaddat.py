import base64
import json

def loadDat():
    dat = ""
    with open("login.logindat", "rb") as f:
        dat = f.read()
        f.close()
    dat = base64.b64decode(dat)
    dat = json.loads(dat.decode())
    return dat[0], dat[1]

print(loadDat())
input()