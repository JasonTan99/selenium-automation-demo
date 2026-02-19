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
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized") 

    # Ensure page_load_strategy doesn't break ChromeDriver
    options.page_load_strategy = "normal"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# -------------------
# Test case example
# -------------------
def test_send_whatsapp_message(driver):
    driver.get("https://web.whatsapp.com")

    try:
        # Wait until WhatsApp is ready
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
    except TimeoutException:
        pytest.fail("⚠️ Session expired, QR scan required")

    # Select second chatroom
    chat_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row']"))
    )
    second_chatroom = chat_list[1]
    second_chatroom.click()

    time.sleep(10)
    # Wait for message field
    message_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @aria-placeholder='Type a message']"))
    )

    # Count messages before sending
    before_sent = len(driver.find_elements(By.XPATH, "//span[@data-testid='selectable-text']"))

    # Type and send message
    message_field.send_keys(Keys.CONTROL + "a")
    message_field.send_keys(Keys.BACKSPACE)
    msg = "test"
    message_field.send_keys(msg)

    send_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-tab='11' and @aria-label='Send']"))
    )
    send_btn.click()


    # Wait until message appears
    try:
        WebDriverWait(driver, 20).until(lambda d: len(d.find_elements(By.XPATH, "//span[@data-testid='selectable-text']")) > before_sent)
        after_sent = len(driver.find_elements(By.XPATH, "//span[@data-testid='selectable-text']"))
        print(f"Messages before: {before_sent}, after: {after_sent}")
        assert after_sent > before_sent, "Message was not sent"
    except TimeoutException:
        pytest.fail("Msg failed to send")
    time.sleep(20)