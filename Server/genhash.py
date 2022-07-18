from hashlib import sha256
import json


def LoadVersionInfo():
	jsondat = ""
	with open("versioninfo.json", "r") as f:
		jsondat = f.read()
	versiondat = json.loads(jsondat)
	return versiondat

verinfo = LoadVersionInfo()
path = verinfo["path"]
data = ""
with open(path, "r") as f:
    data = f.read()

h = sha256(data.encode()).hexdigest()
print(h)
input()