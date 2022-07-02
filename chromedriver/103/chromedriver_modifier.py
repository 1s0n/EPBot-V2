def replace(driverpath):
    with open(driverpath, "rb") as f:
        data = f.read()

    import random

    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def randbytestr(len):
        res = ''.join(random.choice(letters) for i in range(len))
        return res.encode()

    data = data.replace(b"cdc_", randbytestr(4))

    with open(driverpath, "wb") as f:
        f.write(data)
        
    print("Done!")

