# This logs in and get the encryption key from the server
# The main program is encrypted plain python code. Making compiling new updates very easy.
#ClearText
servers = {"MainServer": ("TCP", "us-or-cera-1.natfrp.cloud", "19256"), "DebugServer": ("TCP", "127.0.0.1", "1234"), "DebugOffline": ("TCPLOCAL", "127.0.0.1", "4321")}
verifyserver = {"MainServer": ("TCP")}

#TODO: Implement anti-tampering - DOING
#TODO: Implement auto-updates:

client_data = {
	"version": "1.0.0"
}

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from time import sleep
import os
import socket
import base64

server = servers["DebugServer"]

from tkinter import Tk
from tkinter import simpledialog

if not os.path.basename(__file__) == "main.py":
	debugMode = False

class LocalServer:
	def __init__(self):
		self.SKIP = True

	def connect(self, a1):
		pass

	def send(self, msg):
		if msg == b"CLIENT":
			self.SKIP == True
	
	def recv(self, len):
		print(self.SKIP)
		if self.SKIP == True:
			return "SKIP"

if server[0] == "TCP":
	s = socket.socket()
elif server[0] == "TCPLOCAL":
	s = LocalServer()


import requests
serverpacket = {}
serverpacket["username"] = os.getlogin()

def onexit():
	os._exit(0)

print("Reading login data...")

from gui import getLogin, funcs, MainApp, messagebox, Values

def saveDat(email, password):
	# TODO: implement encryption
	dat = [email, password]
	dat = json.dumps(dat).encode()
	dat = base64.b64encode(dat)
	with open("login.logindat", "wb") as f:
		f.write(dat)
		f.close()
	
def loadDat():
	dat = ""
	with open("login.logindat", "rb") as f:
		dat = f.read()
		f.close()
	dat = base64.b64decode(dat)
	dat = json.loads(dat.decode())
	return dat[0], dat[1]

passwordenc = None

try:
	email, passwordenc = loadDat()
except Exception as e:
	print(e)
	print("Login data doesn't exist or is corrupted!")
	print("Opening login window...")

	email, password = getLogin()
	if email == None or password == None:
		onexit()

print(f"Email: {email}")
print(f"Password: {'*' * len(password)}")	

print(f"Connecting to {server} via {server[0]}")

s.connect(("127.0.0.1", 1234))

print("Setting up encryption stuff...")

from hashlib import sha256
import socket
from time import sleep 
import rsa

from cryptography.fernet import Fernet

s.sendall(b"CLIENT")
print("Starting handshake...")
public_pem = s.recv(1024)

public_key = rsa.PublicKey.load_pkcs1(public_pem)

print("Server public key recived, generating encryption key...")
key = Fernet.generate_key()

fernet = Fernet(key)

keyEnc = rsa.encrypt(key, public_key)

s.sendall(keyEnc)

sec = s.recv(1024)
server_secret = fernet.decrypt(sec)

verhash = server_secret + key
print(verhash)
verhash = sha256(verhash).hexdigest().encode()
print(verhash)
while s.recv(4) == "":
    sleep(0.1)
sleep(1)
vers = socket.socket()
vers.connect(("127.0.0.1", 9821))
vers.sendall(b"2")
vers.sendall(verhash)
resp = vers.recv(6)
vers.close()
if resp == b"ACCEPT":
    print("Handshake data confirmed!")
    print("Handshake complete!")
else:
    print("Handshake hash verification failed!")
    print("Handshake failed! Closing connection...")
    s.close()

encemail = fernet.encrypt(email.encode())

s.sendall(encemail)

enckey = s.recv(1024)
enckey = fernet.decrypt(enckey).decode()

if enckey == "FAILED":
	print("Email doesn't exist!")
	onexit()

f = Fernet(enckey)

if passwordenc != None:
	password = f.decrypt(passwordenc)

loginpacket = {"email": email, "password": password}

logindata = fernet.encrypt(json.dumps(loginpacket).encode())
s.sendall(logindata)

loginresults = s.recv(1024)
loginresults = fernet.decrypt(loginresults)
if loginresults == b"FAILED":
	print("Login failed!")
	onexit()

sha256key = sha256(enckey.encode()).hexdigest().encode()

if sha256key == loginresults:
	print("LOGIN SUCCESS!")
	saveDat(email, )
else:
	print("LOGIN FAILED!")
	print(sha256key)
	print(loginresults)
	s.close()
	onexit()

s.close()