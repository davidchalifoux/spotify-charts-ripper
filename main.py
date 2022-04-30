import time
import os
import datetime
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def get_dates(start_date="2017-1-1"):
    """
    Returns array of dates from Jan 1st 2017 to yesterday
    @param start_date Defaults to 2017-1-1
    """
    # Spotify data starts Jan 1st 2017
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    dates = pd.date_range(start_date, yesterday).tolist()
    return dates


def main():
    # Load ENV variables
    load_dotenv()
    username = os.getenv("SPOTIFY_USERNAME")
    password = os.getenv("SPOTIFY_PASSWORD")

    # Start Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Login to Spotify Charts
    driver.get(
        "https://charts.spotify.com")
    time.sleep(1)
    elem = driver.find_element(By.CLASS_NAME, "jEPoVx")
    elem.click()
    elem = driver.find_element(By.ID, "login-username")
    elem.send_keys(username)
    elem = driver.find_element(By.ID, "login-password")
    elem.send_keys(password + Keys.RETURN)
    time.sleep(1)

    # Collect CSVs
    dates = get_dates()
    for date in dates:
        # Format date to match URL scheme
        date = date.strftime("%Y-%m-%d")
        print("Collecting data for", date)

        # Collect CSV
        driver.get(
            "https://charts.spotify.com/charts/view/regional-us-daily/" + date)
        time.sleep(2)
        elem = driver.find_element(By.CLASS_NAME, "jvhDJQ")
        elem.click()
        time.sleep(2)


main()
