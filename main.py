print("Starting...")
from tkinter import Tk
from selenium import webdriver
import chromedriver_autoinstaller
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from time import sleep
import base64

# TODO: implement contacting server and stuff

print("Detecting os and setting variables...")
import platform
import os

from gui import getLogin, funcs, MainApp, messagebox

system = platform.system()

if system == "Windows":
    datapath = os.getenv('APPDATA') + "\\epbot"
elif system == "Linux":
    datapath = "/var/lib/epbot"
elif system == "Darwin":
    datapath = os.path.expanduser('~') + "/Library/Application Support/epbot"
if not os.path.isdir(datapath): os.mkdir(datapath)

print("Setting more variables...")

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

# Login field
username_selector = "#login-username"
password_selector = "#login-password"
login_button_selector = "#login-submit-button"
login_error_selector = "#content > div.ivu-card.ivu-card-dis-hover.ivu-card-shadow > div > div.inner-login-form.v-group.h-align-center > form > div.v-group.v-align-center > p"

print("Verifying chromedriver/autoinstalling chromedriver...")
chromedriver_autoinstaller.install(path=datapath)

driver = webdriver.Chrome()

def onexit():
    driver.close()
    os._exit(0)



print("Reading login data...")

try:
    email, password = loadDat()
except Exception as e:
    print(e)
    print("Login data doesn't exist or is corrupted!")

    print("Opening login window...")

    email, password = getLogin()
    if email == None or password == None:
        onexit()
print(f"Email: {email}")
print(f"Password: {'*' * len(password)}")

print("Logging in to education perfect...")
driver.get("https://app.educationperfect.com/app/login")

# Wait for it to load

print("Trying to login...")

while True:
    try:
        inputElement = driver.find_element(by=By.CSS_SELECTOR, value=username_selector)
        inputElement.send_keys(email)
        break
    except selenium.common.exceptions.NoSuchElementException:
        sleep(1)

inputElement = driver.find_element(by=By.CSS_SELECTOR, value=password_selector)
inputElement.send_keys(password)

inputElement = driver.find_element(by=By.CSS_SELECTOR, value=login_button_selector)
inputElement.click()

def checkElementExists(css_selector):
    try:
        l = driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
        return True
    except Exception:
        return False

while True:
    try:
        l = driver.find_element(by=By.CSS_SELECTOR, value=login_error_selector)
        s = l.text
        if s == " " or s == "":
            continue
        print(f"Login failed! Exiting...")
        w = Tk()
        w.withdraw()
        messagebox.showerror(title="Login failed", message=f"{s}, Exiting...")
        driver.close()
        onexit()

    except Exception:
        print("Login success (I think)...")
        print("Encrypting and login to disk for quick login...")
        # TODO: Save login using server encryption key and send to server
        saveDat(email, password)
        break

def ScanWords():
    print("Scannign words......")

    wordlist = {} # English : other lang

    if checkElementExists("#full-list-switcher"):
        print("Switching to full list...")

        switchbutton = driver.find_element(by=By.CSS_SELECTOR, value="#full-list-switcher")
        switchbutton.click()
    
    print("Getting words...")

    editButton = driver.find_element(by=By.CSS_SELECTOR, value="#word-count > button.edit-button.ng-binding")
    editButton.click()
    
    # Wait for it to load
    while True:
        try:
            res = driver.find_element(by=By.CSS_SELECTOR, value="#list-edit-selected-list")
            break
        except Exception:
            pass

    print("Reading...")
    options = res.find_elements(by=By.TAG_NAME, value="li")
    for option in options:
        words = option.find_elements(by=By.TAG_NAME, value="div")
        eng = words[1].text
        foreign = words[0].text
        eng = eng.replace(";", ",")
        foreign = foreign.replace(";", ",")
        wordlist[eng] = foreign
    
    print(wordlist)


funcs.scanfunc = ScanWords

app = MainApp(exitfunc=onexit)

print("Starting mainloop...")
while True:
    pass

driver.close()