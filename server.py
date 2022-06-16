print("Starting...")
import socket
import secrets
import sqlite3
import threading
s = socket.socket()
s.bind(("127.0.0.1", 1234))

print("Setting up encryption stuff...")
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives import serialization
_parampem = b'-----BEGIN DH PARAMETERS-----\nMIIBCAKCAQEA0cCWPFextsxjaaOPT0HYHiTocc8nu/DRv3bSJjPPVUox94tVthlx\nDayDuJc4HdKAwqiOICKDEpSTBUsapDn/5R1heR7kVtL525+ioZeDkm2YusyfUW5q\nnLvPqXqecJ1Mx1WnE+PAne8ZAx9shcuiD4sIBhCAYHWaFVPDGak6QuIbGFLIekIa\nG6l8YwS2YfH+bkb8zPt0aOLwjgOolewLVUjD4ap94svYaPWvL8CyVQgmZYTpNCCL\n99fqBLKCKlW6wbGuY6FgcuoU6eCeL6yEUBd0cNUA4ehShVOdefUFSnGFM4KHIsCh\nK5+kI74v6MC3E6UfpjdiXZ0sL+3YxsodBwIBAg==\n-----END DH PARAMETERS-----\n'

# Parameters are not generated each time
parameters = serialization.load_pem_parameters(_parampem)

import json

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt(msg, key):
	iv = None
	cipher = None
	encryptor = None
	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	encryptor = cipher.encryptor()
	ct = encryptor.update(msg) + encryptor.finalize()
	del cipher
	del encryptor
	return ct

def sendenc(conn, msg, key):
	data = encrypt(msg, key)
	conn.sendall(data)

def decrypt(ct, key):
	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	decryptor = cipher.decryptor()
	msg = decryptor.update(ct) + decryptor.finalize()
	return msg

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
		print("Deleting encryption key...")
		cur.execute("INSERT INTO users (email, password) VALUES (?, ?);", (email, password))
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
		print("Beginning encryption handshake...")
		private_key = parameters.generate_private_key()
		public_key = private_key.public_key()

		public_pem = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
		conn.sendall(public_pem)

		print("Reciving public pem...")
		pemdat = conn.recv(1024)
		clientPubic = serialization.load_pem_public_key(pemdat)
		shared_key = private_key.exchange(clientPubic)
		print("Shared Key recived!")
		print("Verifying shared key...")
		derived_key = HKDF(
			algorithm=hashes.SHA256(),
			length=32,
			salt=None,
			info=b'Handshake_Verification',
		).derive(shared_key)
		key2 = conn.recv(len(derived_key))
		if key2 == derived_key:
			print("Handshake complete!")
		else:
			print("KEYERROR!")
			conn.close()
			return

		secret = genKey(64)
		
	conn.close()

print("Listening...")
		
s.listen()

while True:
	c, a = s.accept()
	t = threading.Thread(target=HandleReq, args=(c, a,))
	t.start()