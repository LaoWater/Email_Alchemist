import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from WebScraping_Engine import find_and_click
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



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
    time.sleep(3)
    # Click Login

    # Wait for the login button to become clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='login-button']"))
    )

    # Click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
    login_button.click()

    # Pause to observe actions or wait for next page
    time.sleep(5)

init_browser()
