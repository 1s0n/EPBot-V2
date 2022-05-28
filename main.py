print("Starting...")
from tkinter import Tk
from selenium import webdriver
import chromedriver_autoinstaller
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

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

# Function to call on exit
def onexit():
    os._exit(0)

funcs.exitfunc = onexit

# Login field
username_selector = "#login-username"
password_selector = "#login-password"
login_button_selector = "#login-submit-button"
login_error_selector = "#content > div.ivu-card.ivu-card-dis-hover.ivu-card-shadow > div > div.inner-login-form.v-group.h-align-center > form > div.v-group.v-align-center > p"

print("Verifying chromedriver/autoinstalling chromedriver...")
chromedriver_autoinstaller.install(path=datapath)

print("Opening login window...")

email, password = getLogin()
if email == None or password == None:
    onexit()
print(f"Email: {email}")
print(f"Password: {'*' * len(password)}")

print("Logging in to education perfect...")
driver = webdriver.Chrome()
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
    except selenium.common.exceptions.NoSuchElementException:
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

    except selenium.common.exceptions.NoSuchElementException:
        print("Login success (I think)...")
        print("Saving login to disk for quick login (Encrypted)...")
        # TODO: Save password and send to server
        
        break

def ScanWords():
    print("Scannign words......")
    if checkElementExists("#full-list-switcher"):
        print("Switching to full list...")


funcs.scanfunc = ScanWords

app = MainApp(exitfunc=onexit)

print("Starting mainloop...")
while True:
    pass

driver.close()