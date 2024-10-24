import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


def init_browser():
    """Initialize and return a Chrome browser instance."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    open_page(driver)
    # driver.maximize_window()
    time.sleep(9999999)
    return driver


def open_page(driver):
    """Navigate to the Google Account signup page."""
    driver.get("https://chatgpt.com/")
    time.sleep(1.3)


init_browser()
