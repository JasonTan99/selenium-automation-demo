from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest
import os



# -------------------
# Test case example
# -------------------
def test_login(driver):
    driver.get("https://www.saucedemo.com/")

    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name")))
        print("Page loaded successfully!")
    except TimeoutException:
        print("Page failed to load or element not found.")

    time.sleep(20)