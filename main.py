import socket



print("Starting...")
from multiprocessing.sharedctypes import Value
from random import randint
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

from gui import getLogin, funcs, MainApp, messagebox, Values

system = platform.system()

if system == "Windows":
    datapath = os.getenv('APPDATA') + "\\epbot"
elif system == "Linux":
    datapath = "LINUX"
elif system == "Darwin":
    datapath = os.path.expanduser('~') + "/Library/Application Support/epbot"
if not os.path.isdir(datapath): 
    os.mkdir(datapath)

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

if not datapath == "LINUX":
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

w = Tk()
w.withdraw()
originalPos = driver.get_window_position()
width = w.winfo_screenwidth()

def hideWin():
    return
    global originalPos
    originalPos = driver.get_window_position()
    driver.set_window_position(width + 100, 0)

def showWin():
    return
    driver.set_window_position(originalPos["x"], originalPos["y"])

hideWin()

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
        messagebox.showerror(title="Login failed", message=f"{s}, Exiting...")
        onexit()

    except Exception:
        print("Login success (I think)...")
        print("Encrypting and login to disk for quick login...")
        # TODO: Save login using server encryption key and send to server
        saveDat(email, password)
        break

wordlist = {} # other lang : English
wordlist_reversed = {} # English : other lang

showWin()

def verifyOnTask():
    try:
        if checkElementExists("#full-list-switcher"):
            print("Switching to full list...")

            switchbutton = driver.find_element(by=By.CSS_SELECTOR, value="#full-list-switcher")
            switchbutton.click()
        
        startbutton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
        return True
    except Exception:
        return False
    

def ScanWords():
    global wordlist, wordlist_reversed
    print("Scannign words......")

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

    print("Analyzing...")
    options = res.find_elements(by=By.TAG_NAME, value="li")
    for option in options:
        words = option.find_elements(by=By.TAG_NAME, value="div")
        eng = words[1].text
        foreign = words[0].text
        eng = eng.replace(";", ",")
        foreign = foreign.replace(";", ",")
        wordlist[foreign] = eng
        wordlist_reversed[eng] = foreign
    
    print("Done! Going back...")
    backbutton = driver.find_element(by=By.CSS_SELECTOR, value="#__single_spa_angular_1 > student-app-wrapper > div.main-content.v-group > div.nav-bar-dashboard.tight.ep-nav-bar.ng-isolate-scope > div > div > div.back-action.h-group.nav-bar-button.v-align-center.ng-scope")
    backbutton.click()

def quitTask():
    backButton = driver.find_element(by=By.CSS_SELECTOR, value="#action-bar > div > div.start > button")
    backButton.click()
    backButton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
    backButton.click()

def doReading():
    global wordlist
    print("Doing reading...")
    try:
        taskbutton = driver.find_element(by=By.CSS_SELECTOR, value="#learning-mode-selector > li.item.h-group.v-align-center.mode-0")
    except Exception:
        try:
            taskbutton = driver.find_element(by=By.CSS_SELECTOR, value="#learning-mode-selector > li.item.h-group.v-align-center.mode-0.selected")
        except Exception as e:
            messagebox.showerror(title="Fatal Error", message=f"An Error Occured, Error: \n" + str(e))
            # TODO: Report fatal error to server
            onexit()
    
    taskbutton.click()
    startbutton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
    startbutton.click()

    while True:
        if Values.running == False:
            sleep(0.2)
            continue
        
        try:
            wordElement = driver.find_element(by=By.CSS_SELECTOR, value="#question-text")
            inputElement = driver.find_element(by=By.XPATH, value="/html/body/div[2]/main[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div[1]/div[2]/div/div/div[2]/div[2]/game-lp-answer-input/div/div[2]/input")
            submitElement = driver.find_element(by=By.CSS_SELECTOR, value="#submit-button")
        except Exception as e:
            try:
                finishButton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
                showWin()
            except Exception as e:
                print("User on unknown page!")
                messagebox.showerror(title="Fatal Error", message=f"An Error Occured, Error: \n" + str(e))
                # TODO: Report fatal error to server
                onexit()

        # print(wordElement.text)

        makemistake = False

        question = wordElement.text

        if randint(1, Values.error_rate) == 1:
            makemistake = True

        if question in wordlist and not makemistake:
            # print(wordlist)
            ans = wordlist[question]
            ans = ans.split(",")[0]
            for character in ans:
                inputElement.send_keys(character)
                sleep(Values.typing_speed)

            submitElement.click()
        else:
            # Learn the word
            print("Unknown word " + question + " learning...")
            inputElement.send_keys("?")
            sleep(0.2)
            submitElement.click()
            sleep(0.5)
            if not makemistake:
                correctansField = driver.find_element(by=By.CSS_SELECTOR, value="#correct-answer-field")
                wordlist[question] = correctansField.text
                # print(correctansField.text)
            skipButton = driver.find_element(by=By.CSS_SELECTOR, value="#viewport > div.modal.lp-hint-dialog.center-modal.fade.ng-scope.ng-isolate-scope.in > div > div > div.modal-footer.ng-scope > button")
            sleep(0.5)
            skipButton.click()

        sleep(Values.rest_in_between_questions)

def doWriting():
    print("Doing writing...")
    try:
        taskbutton = driver.find_element(by=By.CSS_SELECTOR, value="#learning-mode-selector > li.item.h-group.v-align-center.mode-1")
    except Exception:
        try:
            taskbutton = driver.find_element(by=By.CSS_SELECTOR, value="#learning-mode-selector > li.item.h-group.v-align-center.mode-1.selected")
        except Exception as e:
            messagebox.showerror(title="Fatal Error", message=f"{s}, An Error Occured, Error: \n" + str(e))
            # TODO: Report fatal error to server
            onexit()
    
    taskbutton.click()
    startbutton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
    startbutton.click()

    while True:
        if Values.running == False:
            sleep(0.2)
            continue
        
        try:
            wordElement = driver.find_element(by=By.CSS_SELECTOR, value="#question-text")
            inputElement = driver.find_element(by=By.XPATH, value="/html/body/div[2]/main[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div[1]/div[2]/div/div/div[2]/div[2]/game-lp-answer-input/div/div[2]/input")
            submitElement = driver.find_element(by=By.CSS_SELECTOR, value="#submit-button")
        except Exception as e:
            try:
                finishButton = driver.find_element(by=By.CSS_SELECTOR, value="#start-button-main")
                showWin()
            except Exception as e:
                print("User on unknown page!")
                messagebox.showerror(title="Fatal Error", message=f"An Error Occured, Error: \n" + str(e))
                # TODO: Report fatal error to server
                onexit()

        # print(wordElement.text)

        makemistake = False

        question = wordElement.text

        if randint(1, Values.error_rate) == 1:
            makemistake = True

        if question in wordlist_reversed and not makemistake:
            # print(wordlist)
            ans = wordlist_reversed[question]
            ans = ans.split(",")[0]
            for character in ans:
                inputElement.send_keys(character)
                sleep(Values.typing_speed)

            submitElement.click()
        else:
            # Learn the word
            print("Unknown word " + question + " learning...")
            inputElement.send_keys("?")
            sleep(0.2)
            submitElement.click()
            sleep(0.5)
            if not makemistake:
                correctansField = driver.find_element(by=By.CSS_SELECTOR, value="#correct-answer-field")
                wordlist_reversed[question] = correctansField.text
                # print(correctansField.text)
            skipButton = driver.find_element(by=By.CSS_SELECTOR, value="#viewport > div.modal.lp-hint-dialog.center-modal.fade.ng-scope.ng-isolate-scope.in > div > div > div.modal-footer.ng-scope > button")
            sleep(0.5)
            skipButton.click()

        sleep(Values.rest_in_between_questions)
    

funcs.scanfunc = ScanWords
funcs.readingfunc = doReading
funcs.writingfunc = doWriting
funcs.hidewindow = hideWin
funcs.showwindow = showWin
funcs.verifyontask = verifyOnTask
funcs.stoptask = quitTask

app = MainApp(exitfunc=onexit)

print("Starting mainloop...")
w.mainloop()