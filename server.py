print("Starting...")
import socket

s = socket.socket()
s.bind(("127.0.0.1", 1234))


print("Setting up encryption stuff...")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decodePublicKey(pem):
    public_key = serialization.load_pem_public_key(
        pem,
        backend=default_backend()
    )
    return public_key

def encrypt(message, public_key):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted

def decrypt(encrypted, private_key):
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return original_message


def HandleReq():
    print("Beginning encryption handshake...")
    verifytoken = secrets.token_hex(16)
    print("Verification token: " + verifytoken)
    
    conn.sendall(f"{verifytoken}:::{public_pem.decode()}".encode())
    
    encryptiondata = conn.recv(4096)

    print("Encrypted data recived, Reading...")
    data = decrypt(encryptiondata, private_key).decode()
    data = data.split(":::")
    enc_key = data[0]
    token = data[1]
    print("Verifying token... ", end = "")
    if not token == verifytoken:
        print("FAILED, prob bec of an unwanted proxy on client pc. \nClosing connection...")
        conn.close()
    print("SUCCESS!")
    print("Handshake complete!")
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()