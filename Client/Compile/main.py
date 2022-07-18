#ClearText
servers = {"MainServer": ("TCP", "us-or-cera-1.natfrp.cloud", "19256"), "DebugServer": ("TCP", "127.0.0.1", "9128"), "DebugOffline": ("TCPLOCAL", "127.0.0.1", "4321")}
verifyserver = {"MainServer": ("TCP")}

import email
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

import platform

system = platform.system()

if system == "Windows":
	datapath = "chromedriver"
elif system == "Linux":
	datapath = "/chromedriver/"
elif system == "Darwin":
	datapath = "/chromedriver/"
if not os.path.isdir(datapath) and not datapath == "": 
	os.mkdir(datapath)

from gui import getLogin, funcs, MainApp, messagebox, Values
from tkinter import Tk
from tkinter import simpledialog
w = Tk()
w.withdraw()
w.attributes('-topmost',1)

print("Starting Bot...")

print("Detecting os and setting variables...")


print("Setting more variables...")

def onexit():
	driver.quit()
	os._exit(0)

if not datapath == "LINUX":
	print("Verifying chromedriver/autoinstalling chromedriver...")
	print(datapath)
	chromedriver_autoinstaller.install(path=datapath)


def hideWin():
	return
	global originalPos
	originalPos = driver.get_window_position()
	driver.set_window_position(width + 100, 0)

def showWin():
	return
	driver.set_window_position(originalPos["x"], originalPos["y"])

hideWin()


# Login field

email = "{email}"
password = "{password}"

username_selector = "#login-username"
password_selector = "#login-password"
login_button_selector = "#login-submit-button"
login_error_selector = "#content > div.ivu-card.ivu-card-dis-hover.ivu-card-shadow > div > div.inner-login-form.v-group.h-align-center > form > div.v-group.v-align-center > p"


driver = webdriver.Chrome()

print("Logging in to education perfect...")
driver.get("https://app.educationperfect.com/app/login")

originalPos = driver.get_window_position()
width = w.winfo_screenwidth()

print("Trying to login...")

# Wait for it to load
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
	print("STOPTASK")

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
	startbutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/main[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[1]/div[4]/button")
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
		if not Values.error_rate == 0:
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

def doDefault():
	global wordlist
	print("Doing default...")
	startbutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/main[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[1]/div[4]/button")
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
		if not Values.error_rate == 0:
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
funcs.defaultfunc = doDefault
funcs.writingfunc = doWriting
funcs.hidewindow = hideWin
funcs.showwindow = showWin
funcs.verifyontask = verifyOnTask
funcs.stoptask = quitTask

app = MainApp(exitfunc=onexit)

FakeFocusScript = """

const script = document.createElement('script');
script.dataset.hidden = document.hidden;
script.addEventListener('state', () => {
  script.dataset.hidden = document.hidden;
});

script.textContent = `{
  const script = document.currentScript;
  const isFirefox = /Firefox/.test(navigator.userAgent) || typeof InstallTrigger !== 'undefined';

  const block = e => {
	e.preventDefault();
	e.stopPropagation();
	e.stopImmediatePropagation();
  };

  /* visibility */
  Object.defineProperty(document, 'visibilityState', {
	get() {
	  return 'visible';
	}
  });
  if (isFirefox === false) {
	Object.defineProperty(document, 'webkitVisibilityState', {
	  get() {
		return 'visible';
	  }
	});
  }
  document.addEventListener('visibilitychange', e => {
	script.dispatchEvent(new Event('state'));
	if (script.dataset.visibility !== 'false') {
	  return block(e);
	}
  }, true);
  document.addEventListener('webkitvisibilitychange', e => script.dataset.visibility !== 'false' && block(e), true);
  window.addEventListener('pagehide', e => script.dataset.visibility !== 'false' && block(e), true);

  /* hidden */
  Object.defineProperty(document, 'hidden', {
	get() {
	  return false;
	}
  });
  Object.defineProperty(document, isFirefox ? 'mozHidden' : 'webkitHidden', {
	get() {
	  return false;
	}
  });

  /* focus */
  document.addEventListener('hasFocus', e => script.dataset.focus !== 'false' && block(e), true);
  document.__proto__.hasFocus = new Proxy(document.__proto__.hasFocus, {
	apply(target, self, args) {
	  if (script.dataset.focus !== 'false') {
		return true;
	  }
	  return Reflect.apply(target, self, args);
	}
  });

  /* blur */
  const onblur = e => {
	if (script.dataset.blur !== 'false') {
	  if (e.target === document || e.target === window) {
		return block(e);
	  }
	}
  };
  document.addEventListener('blur', onblur, true);
  window.addEventListener('blur', onblur, true);

  /* mouse */
  window.addEventListener('mouseleave', e => {
	if (script.dataset.mouseleave !== 'false') {
	  if (e.target === document || e.target === window) {
		return block(e);
	  }
	}
  }, true);

  /* requestAnimationFrame */
  let lastTime = 0;
  window.requestAnimationFrame = new Proxy(window.requestAnimationFrame, {
	apply(target, self, args) {
	  if (script.dataset.hidden === 'true') {
		const currTime = Date.now();
		const timeToCall = Math.max(0, 16 - (currTime - lastTime));
		const id = window.setTimeout(function() {
		  args[0](performance.now());
		}, timeToCall);
		lastTime = currTime + timeToCall;
		return id;
	  }
	  else {
		return Reflect.apply(target, self, args);
	  }
	}
  });
  window.cancelAnimationFrame = new Proxy(window.cancelAnimationFrame, {
	apply(target, self, args) {
	  if (script.dataset.hidden === 'true') {
		clearTimeout(args[0]);
	  }
	  return Reflect.apply(target, self, args);
	}
  });

}`;
document.documentElement.appendChild(script);
script.remove();
const update = () => chrome.storage.local.get({
  'blur': true,
  'focus': true,
  'mouseleave': true,
  'visibility': true,
  'policies': null
}, prefs => {
  let hostname = location.hostname;
  try {
	hostname = parent.location.hostname;
  }
  catch (e) {}

  prefs.policies = prefs.policies ?? {};
  const policy = prefs.policies[hostname] || [];

  script.dataset.blur = policy.indexOf('blur') === -1 ? prefs.blur : false;
  script.dataset.focus = policy.indexOf('focus') === -1 ? prefs.focus : false;
  script.dataset.mouseleave = policy.indexOf('mouseleave') === -1 ? prefs.mouseleave : false;
  script.dataset.visibility = policy.indexOf('visibility') === -1 ? prefs.visibility : false;
});
update();
chrome.storage.onChanged.addListener(update);
"""

driver.execute_script(FakeFocusScript)

w.mainloop()