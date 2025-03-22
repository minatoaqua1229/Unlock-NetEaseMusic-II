# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U="00C9C60DE87C7D38F5E1F9988F8687876F2C576D33B12834EA726CA1E2E6C4A1F3CCA9A85D2339C96E46216C2528A5E3104F7F5D6325C5A3D2738FE01A4DCC89B71618D1235CB0EFED231CBD1ABB97B242CA1070D6D4AD2DC4EF3BD551BAF15437C3A3405B477926B51C501A6092A3425B3ADEE803341FACF25408EACEF5422B7E1126F353EFD40DB159C1985B39125A1C0BB5B814157372F263F3A9B74E65DE843A3A1C7E37D19420FBF3B576FA1780C7DDB4ABF3E1BD1857FB5DB8741CD18E9C5E60F3265654845D500CCF7FF2EE4F596BDE68457A2D12CF86A510B6D8C9415BE64CFF098DAFA65F50FAD7D4692CEC88214B7DDDBBC81F161D67E75F0ED09460285D752E3D8F830D7FA08D981B02A8D49532C3C179464ED2CDFFD6DEBF9C375546D21F636EFE014875ECD5CAE6F85093B3E822DCA2C272637BC6EC76A28A120E84B4858B95C01C4B0FACA43367784190A92CB147EF26156D6643183E7BE3DDAD

    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
