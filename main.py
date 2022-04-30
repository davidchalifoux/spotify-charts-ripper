import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Load ENV variables
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Spotify data starts Jan 1st 2017

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://charts.spotify.com/charts/view/regional-us-daily/2022-04-29")
time.sleep(1)
elem = driver.find_element_by_class_name("jEPoVx")
elem.click()
elem = driver.find_element_by_id("login-username")
elem.send_keys(username)
elem = driver.find_element_by_id("login-password")
elem.send_keys(password + Keys.RETURN)
time.sleep(1)
driver.get("https://charts.spotify.com/charts/view/regional-us-daily/2022-04-29")
time.sleep(1)
elem = driver.find_element_by_class_name("jvhDJQ")
elem.click()
time.sleep(120)
