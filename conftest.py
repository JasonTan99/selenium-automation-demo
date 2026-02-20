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
# Pytest fixture: setup & teardown Chrome
# -------------------
@pytest.fixture(scope="module")
def driver():
    profile_path = "/Users/tanjiansheng/websession"
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    options = Options()
    #options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized") 

    # Ensure page_load_strategy doesn't break ChromeDriver
    options.page_load_strategy = "normal"

    #ChromeDriver is the “translator” between Selenium and Chrome.
    #Normally, you have to download it manually and tell Selenium where it is.
    #ChromeDriverManager().install() → automatically downloads the right ChromeDriver for your Chrome version.
    service = Service(ChromeDriverManager().install()) 
    
    #open browser
    #service=service → uses the ChromeDriver we just prepared
    #options=options → sets things like “start maximized”
    driver = webdriver.Chrome(service=service, options=options) 
    
    yield driver #return webdriver instance to test function
    driver.quit()