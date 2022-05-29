from tkinter import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
w = Tk()
w.withdraw()
width = w.winfo_screenwidth()
originalPos = driver.get_window_position()
sleep(2)
driver.set_window_position(width + 100, 0)
sleep(1)
driver.set_window_position(originalPos["x"], originalPos["y"])
sleep(1)
driver.set_window_position(width + 100, 0)
sleep(1)
driver.set_window_position(originalPos["x"], originalPos["y"])
driver.close()