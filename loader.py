servers = {"MainServer": ("TCP", "us-or-cera-1.natfrp.cloud", "19256"), "DebugServer": ("TCP", "127.0.0.1", "1234"), "DebugOffline": ("TCPLOCAL", "127.0.0.1", "4321")}
verifyserver = {"MainServer": ("TCP")}

from random import randint
from selenium import webdriver
import chromedriver_autoinstaller
import selenium
import hashlib

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

import platform

system = platform.system()

if system == "Windows":
	datapath = os.getenv('APPDATA') + "\\epbot"
elif system == "Linux":
	datapath = ""
elif system == "Darwin":
	datapath = os.path.expanduser('~') + "/Library/Application Support/epbot"
if not os.path.isdir(datapath) and not datapath == "": 
	os.mkdir(datapath)


import requests
serverpacket = {}
serverpacket["username"] = os.getlogin()

def onexit():
	os._exit(0)

print("Reading login data...")

from gui import getLogin, funcs, MainApp, messagebox, Values

def saveDat(email, password):
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
	password = f.decrypt(passwordenc.encode()).decode()

print(f"Password: {'*' * len(password)}")

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
	saveDat(email, f.encrypt(password.encode()).decode())
else:
	print("LOGIN FAILED!")
	print(sha256key)
	print(loginresults)
	s.close()
	onexit()

print("Loading client data")

client_data = {
	"version": "0.0.0",
	"release": 0
}

if os.path.isfile("bin/epbot.dat"):
	with open("bin/epbot.dat", "rb") as f:
		epbot_data = f.read()

	cli_dat = epbot_data.split(b"|SPLIT|")[0]

	cli_dat = base64.b64decode(cli_dat)

	client_data = json.loads(cli_dat.decode())

dat = json.dumps(client_data)
dat = dat.encode()
dat = fernet.encrypt(dat)
s.send(dat)

resp = s.recv(1024)
resp = fernet.decrypt(resp)

if resp == b"UPDATE_REQUEST":
	print("Client needs updating!")
	print("Updating client...")
	s.send(b"a")
	update_len = s.recv(1024)
	update_len = fernet.decrypt(update_len)
	update_len = int(update_len)
	print(f"Update length: {update_len / 1000} KB")
	s.send(b"a")
	print("Downloading...")
	update_data = s.recv(update_len + 10)
	print(print("Writing update data..."))

	if not os.path.isdir("bin"):
		os.mkdir("bin")

	with open("bin/epbot.dat", "wb") as f:
		f.write(update_data) 

	print("Update finished!")
	messagebox.showinfo("SUCCESS", "Update success! Please reopen the client to continue.")
	onexit()
elif resp == b"LOGIN_SUCCESS":
	s.send(b"a")
	enckey2 = s.recv(1024)
	print("Recived encryption key!")

s.close()

# print(server_pem)

print("Login success! Starting client...")
enckey2 = fernet.decrypt(enckey2)

epbot_data = ""

if os.path.isfile("bin/epbot.dat"):
	with open("bin/epbot.dat", "rb") as f:
		epbot_data = f.read()
	epbot_data = epbot_data.split(b"|SPLIT|")[1]
	fer = Fernet(enckey2)
	epbot_data = fer.decrypt(epbot_data)
	epbot_data = epbot_data.decode()
elif os.path.isfile("main.py"):
	with open("bin/epbot.dat", "r") as f:
		epbot_data = f.read()

epbot_data = epbot_data.format(email=email, password=password)
exec(epbot_data)