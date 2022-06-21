print("Starting...")
from hashlib import md5
import socket
import secrets
import sqlite3
import threading
from cryptography.fernet import Fernet
import rsa
s = socket.socket()
s.bind(("127.0.0.1", 1234))

# TODO: Implement logging

print("Setting up encryption stuff...")

import json

import os

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
	cur.execute("SELECT data FROM tokens WHERE data = ?", (license,))
	results = cur.fetchall()
	if len(license) < 1:
		return json.dumps({"FAILED": "Creation failed"})
	print(results[0][0])
	if results[0][0] == license:
		print("License found!")
		print("Deleting license key and generating encryption key...")
		enckey = Fernet.generate_key().decode()
		cur.execute("INSERT INTO users (email, password, enckey) VALUES (?, ?, ?);", (email, password, enckey,))
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

print("Generating new encryption keys...")

public_key, private_key = rsa.newkeys(2048)

print("Getting pem of public key...")
public_pem = public_key.save_pkcs1('PEM')

def HandleReq(conn, addr):
	print("Accepted!")
	header = conn.recv(1024).decode()
	header.replace("\r", "")
	headers = header.split("\n")
	reqDat = headers[0].split(" ")

	if reqDat[0] == "GET":
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
		conn.sendall(public_pem)

		keyEnc = conn.recv(256)

		key = rsa.decrypt(keyEnc, private_key)

		fernet = Fernet(key)

		sec = secrets.token_hex(32).encode()

		conn.sendall(fernet.encrypt(sec))

		print("Confirming handshake hash with backup server...")

		verhash = sec + key
		print(verhash)
		verhash = md5(verhash).hexdigest().encode() 
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
		cur.execute("SELECT (enckey) FROM users WHERE (email, password) = (?, ?);", (email, password,))
		res = cur.fetchone()
		if res == None:
			print("FAILED")
			conn.send(fernet.encrypt(b"FAILED"))
		else:
			data = res[0].encode()
			data = md5(data).hexdigest()
			data = data.encode()
			data = fernet.encrypt(data)
			print(res)
			conn.send(data)
	conn.close()

print("Listening...")
		
s.listen()

while True:
	c, a = s.accept()
	t = threading.Thread(target=HandleReq, args=(c, a,))
	t.start()