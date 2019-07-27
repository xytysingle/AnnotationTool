from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import json


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

getLogin_url = 'https:www.baidu.com'
browser.get(getLogin_url)

browser.execute_script("localStorage.setItem('car', 3)")
key = "'car'"
car = browser.execute_script("return localStorage.getItem({})".format(key))

print(car)