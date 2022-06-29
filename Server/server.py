print("Starting...")
from hashlib import sha256
import socket
import secrets
import sqlite3
import threading
import time
import uuid
from cryptography.fernet import Fernet
import jwt
import rsa
import logging
from datetime import datetime, timezone
import base64

"""
dt = datetime( 2021, 3, 5, 14, 30, 21, tzinfo=timezone.utc )
timestamp = int( dt.timestamp() )
print( timestamp )
"""

# TODO: Implement auto-updates...
#TODO: Make Website

Log_Format = "[%(levelname)s][%(asctime)s] %(message)s"

logging.basicConfig(filename = "server.log",
                    filemode = "w",
                    format = Log_Format)

logger = logging.getLogger()

logger.info("Logger setup finished!")

s = socket.socket()
s.bind(("127.0.0.1", 1234))

import json

def getdate():
	return time.time()
    
logger.info("Defining functions...")

def testecho(headers, data):
	data += "TESTECHO!"
	return data.encode()

import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def checkemail(email):
	if(re.fullmatch(regex, email)):
		return True
	else:
		return False

def activateAccount(headers, data):
	# Post request payload example: payload = {"email":"jason@gmail.com", "password": "p@ssword", "license": "ikAWYTeMN7KftBHEkdbNto8ykSCtXJnL"}
	logger.info("Account activation request")
	try:
		c = headers["Content-Type"].split(";")[0]
		if c != "application/json":
			return json.dumps({"ERROR": "Content-Type header is not application/json!"})
	except KeyError:
		return json.dumps({"ERROR": "Content-Type header doesn't exist!"})
	
	try:
		jsondat = json.loads(data)
	except:
		return json.dumps({"ERROR": "Json data parsing failed!"})
	
	try:
		email = jsondat["email"]
		password = jsondat["password"]
		license = jsondat["license"]
	except:
		return json.dumps({"ERROR": "Json data parsing failed!"})
	
	if checkemail(email) == False:
		return json.dumps({"FAILED": "Invaliad Email!"})

	print("Loading sql database...")
	con = sqlite3.connect('license.db')
	cur = con.cursor()
	cur.execute("SELECT data, length FROM tokens WHERE data = ?", (license,))
	results = cur.fetchall()
	if len(license) < 1:
		return json.dumps({"FAILED": "Creation failed"})
	print(results[0][0])
	print(results[0])
	if results[0][0] == license:
		print("License found!")
		print(f"License length: {results[0][1]} days")
		print("Deleting license key and generating encryption key...")
		enckey = Fernet.generate_key().decode()
		enckey2 = enckey = Fernet.generate_key().decode()
		expirydate = getdate() + (results[0][1] * 86400) # 86400 = 24*60*60
		date = datetime.fromtimestamp(expirydate)
		m = date.month
		y = date.year
		d = date.day
		print(f"License expiring on: {d}/{m}/{y}")
		token = secrets.token_hex(32)
		cur.execute("INSERT INTO users (email, password, enckey, enckey2, expirydate, token) VALUES (?, ?, ?, ?, ?, ?);", (email, password, enckey, enckey2, expirydate, token,))
		cur.execute("DELETE FROM tokens WHERE data = ?;", (license,))
	else:
		return json.dumps({"FAILED": "Creation failed"})

	con.commit()
	con.close()

	return json.dumps({"SUCCESS": "Account created!"})

postrequestpaths = {
	"/testecho/": testecho,
	"/activate/": activateAccount
}

from genlicense import genKey


logger.info("Generating encryption keys...")
print("Generating new encryption keys...")

public_key, private_key = rsa.newkeys(2048)

print("Getting pem of public key...")
public_pem = public_key.save_pkcs1('PEM')

sessions = {}

class SessionData:
	def __init__(self, email, password):
		self.email = email
		self.password = password

def LoadVersionInfo():
	jsondat = ""
	with open("versioninfo.json", "r") as f:
		jsondat = f.read()
	versiondat = json.loads(jsondat)
	return versiondat

def waitTillConfirm(conn, data=b"a"):
	while True:
		a = conn.recv(1)
		if a == data:
			break
		time.sleep(0.5)

def HandleReq(conn, addr):
	print("Accepted!")
	header = conn.recv(1024).decode()
	header.replace("\r", "")
	headers = header.split("\n")
	reqDat = headers[0].split(" ")

	if reqDat[0] == "GET":
		logger.debug("New GET request from " + addr[0] + ":" + addr[1])
		conn.sendall(b"HTTP/1.1 400 Bad Request")
		conn.close()
	
	if reqDat[0] == "POST":
		# print(addr)
		# Handle post request
		print("POST REQ")
		req = header

		reqdat = req.split("\r\n\r\n")
		# print(reqdat)
		reqheader = reqdat[0]
		reqdata = reqdat[1]
		reqheader = reqheader.splitlines()
		reqinf = reqheader[0]
		reqheader.pop(0)

		headers = {}

		for header in reqheader:
			header = header.split(": ")
			headers[header[0]] = header[1]
		

		reqpath = reqDat[1]

		if reqpath[len(reqpath) - 1] != "/":
			reqpath += "/"

		responsedat = postrequestpaths[reqpath](headers, reqdata)
		
		conn.sendall(f"HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\r\n\r\n{responsedat}".encode())
		conn.close()

	elif reqDat[0] == "CLIENT":
		logger.debug("Client login request from " + addr[0])
		conn.sendall(public_pem)

		keyEnc = conn.recv(256)

		key = rsa.decrypt(keyEnc, private_key)

		fernet = Fernet(key)

		sec = secrets.token_hex(32).encode()

		conn.sendall(fernet.encrypt(sec))

		print("Confirming handshake hash with backup server...")

		verhash = sec + key
		print(verhash)
		verhash = sha256(verhash).hexdigest().encode() 
		print(verhash)
		vers = socket.socket()
		vers.connect(("127.0.0.1", 9821))
		vers.sendall(b"1")
		vers.sendall(verhash)
		conn.send(b"send")
		resp = vers.recv(6)
		vers.close()
		if resp == b"ACCEPT":
			print("Handshake data confirmed!")
			print("Handshake complete!")
		else:
			print("Handshake hash verification failed!")
			print("Handshake failed! Closing connection...")
			conn.close()
		
		email = conn.recv(1024)
		email = fernet.decrypt(email).decode()
		print("Request email " + email)
		con = sqlite3.connect('license.db')
		cur = con.cursor()
		cur.execute("SELECT enckey FROM users WHERE email = ?;", (email,))
		dat = cur.fetchone()
		if dat != None:
			dat = dat[0]
		print(dat)
		if dat == None:
			conn.send(fernet.encrypt(b"FAILED"))
		else:
			conn.send(fernet.encrypt(dat.encode()))
		logindat = conn.recv(1024)
		print(type(logindat))
		logindat = fernet.decrypt(logindat)
		loginjson = json.loads(logindat)
		if "email" in loginjson and "password" in loginjson:
			password = loginjson["password"]

		cur.execute("SELECT enckey, enckey2 FROM users WHERE (email, password) = (?, ?);", (email, password,))
		res = cur.fetchone()

		if res == None:
			print("FAILED")
			conn.send(fernet.encrypt(b"FAILED"))
		else:
			data = res[0].encode()
			data = sha256(data).hexdigest()
			data = data.encode()
			data = fernet.encrypt(data)
			print(res)
			conn.send(data)

		cli_data = conn.recv(1024)
		client_data = fernet.decrypt(cli_data)
		client_data = json.loads(client_data)

		client_version = client_data["version"]
		client_build_no = client_data["release"]

		versiondat = LoadVersionInfo()
		latest_build = versiondat["version"]
		latest_buildid = versiondat["release"]
		if latest_buildid > client_build_no:
			print("Client needs updating!")
			conn.send(fernet.encrypt(b"UPDATE_REQUEST"))
			waitTillConfirm(conn)
			print("Reading update data...")
			updatefile = versiondat["path"]
			updatedata = ""
			update_key = res[1].encode()
			print(update_key)
			f = Fernet(update_key)
			with open(updatefile, "r") as fi:
				updatedata = fi.read()
			update_info = {
				"version": versiondat["version"],
				"release": versiondat["release"]
			}
			update_info = json.dumps(update_info)
			update_info = update_info.encode()
			updatedata = f.encrypt(updatedata.encode())
			updatedata = base64.b64encode(update_info) + b"|SPLIT|" + updatedata
			conn.send(fernet.encrypt(str(len(updatedata)).encode()))
			print(f"Sent len of updatedata: {len(updatedata)}")
			waitTillConfirm(conn)
			conn.send(updatedata)
			print("update finished!")
			conn.close()
			return
			
		print("Login success!")
		update_key = res[1].encode()
		conn.send(fernet.encrypt(b"LOGIN_SUCCESS"))
		waitTillConfirm(conn)
		conn.send(fernet.encrypt(update_key))
	elif reqDat[0] == "CLIENT2":
		logger.debug("Bot client login request from " + addr[0])
		conn.sendall(public_pem)

		keyEnc = conn.recv(256)

		key = rsa.decrypt(keyEnc, private_key)

		fernet = Fernet(key)

		sec = secrets.token_hex(32).encode()

		conn.sendall(fernet.encrypt(sec))

		print("Confirming handshake hash with backup server...")

		verhash = sec + key
		print(verhash)
		verhash = sha256(verhash).hexdigest().encode() 
		print(verhash)
		vers = socket.socket()
		vers.connect(("127.0.0.1", 9821))
		vers.sendall(b"1")
		vers.sendall(verhash)
		conn.send(b"send")
		resp = vers.recv(6)
		vers.close()
		if resp == b"ACCEPT":
			print("Handshake data confirmed!")
			print("Handshake complete!")
		else:
			print("Handshake hash verification failed!")
			print("Handshake failed! Closing connection...")
			conn.close()
		


	conn.close()

print("Listening...")
logger.info("Listening for connections...")
s.listen()

failed_requests = {}

def HandleReqSafe(c, a):
	try:
		if failed_requests[a] > 10:
			c.close()
	except KeyError:
		failed_requests[a] = 0
	try:
		HandleReq(c, a)
	except Exception as e:
		c.close()
		failed_requests[a] += 1
		raise e
	failed_requests[a] = 0

while True:
	c, a = s.accept()
	t = threading.Thread(target=HandleReqSafe, args=(c, a,))
	t.start()