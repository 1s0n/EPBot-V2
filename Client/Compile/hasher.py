from base64 import b64encode
import hashlib
import os


def get_hash(directory=""):
    hashes = []

    def get_files(path=""):
        nonlocal hashes
        files = []
        if os.path.isfile(path):
            return path
        if os.path.basename(path) == "bin":
            return []
        for file in os.listdir(path):
            if os.path.isfile(path + file):
                files.append(file)
            else:
                if os.path.isfile("".join(get_files(path + "/" + file))):
                    with open("".join(get_files(path + "/" + file)), "rb") as f:
                        hashes.append(hashlib.sha256(f.read()))
                    files.append("".join(get_files(path + "/" + file)))
        return files
    get_files(directory)
    return hashes

if __name__ == "__main__":

    hashes = get_hash("loader.dist")
    bighash = ""
    for i in hashes:
        bighash += i.hexdigest()

    hash = hashlib.sha256(bighash.encode())
    print(hash.hexdigest())