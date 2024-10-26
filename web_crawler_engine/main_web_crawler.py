import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from WebScraping_Engine import find_and_click


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
    # Call the find_and_click function with your specific paths and outer_html
    find_and_click(
        driver,
        outer_html='<button class="btn relative btn-primary btn-small" data-testid="login-button"><div class="flex items-center justify-center">Log in</div></button>',  # Provide the actual outerHTML here
        full_xpath="/html/body/div[1]/div[1]/div[1]/div[3]/button",
        selector="body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > div.draggable.sticky.top-0.z-10.flex.min-h-\[60px\].items-center.justify-center.border-transparent.bg-token-main-surface-primary.pl-0.md\:hidden > div.no-draggable.absolute.bottom-0.right-0.top-0.mr-3.inline-flex.items-center.justify-center > button",
        js_path='document.querySelector("body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > div.draggable.sticky.top-0.z-10.flex.min-h-\\[60px\\].items-center.justify-center.border-transparent.bg-token-main-surface-primary.pl-0.md\\:hidden > div.no-draggable.absolute.bottom-0.right-0.top-0.mr-3.inline-flex.items-center.justify-center > button")',
        iframe_selector=None  # Replace with your iframe selector if needed
    )


init_browser()
