from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException
)
from bs4 import BeautifulSoup
import time
from selenium import webdriver


def generate_locator_strategies(outer_html=None, full_xpath=None, selector=None):
    """
    Generate a list of locator strategies based on the provided inputs.

    Parameters:
    - outer_html: The outer HTML of the target element (string).
    - full_xpath: The full XPath of the element.
    - selector: The CSS selector of the element.

    Returns:
    - A list of tuples containing (By method, selector string).
    """
    strategies = []

    # Add provided selector strategies
    if selector:
        strategies.append((By.CSS_SELECTOR, selector))
        print(f"📌 Added CSS Selector strategy: {selector}")

    if full_xpath:
        strategies.append((By.XPATH, full_xpath))
        print(f"📌 Added Full XPath strategy: {full_xpath}")

    # Parse outer_html to extract attributes and generate additional strategies
    if outer_html:
        print("📝 Parsing outer HTML to extract attributes for additional strategies.")
        soup = BeautifulSoup(outer_html, 'html.parser')
        element = soup.find()  # Get the first (and presumably only) element

        if element:
            tag = element.name
            element_id = element.get('id')
            classes = element.get('class', [])
            attributes = element.attrs
            text = element.get_text(strip=True)

            print(f"🔍 Extracted Tag: {tag}")
            print(f"🔍 Extracted ID: {element_id}")
            print(f"🔍 Extracted Classes: {classes}")
            print(f"🔍 Extracted Attributes: {attributes}")
            print(f"🔍 Extracted Text: {text}")

            # If ID is present, use it
            if element_id:
                strategies.append((By.ID, element_id))
                print(f"📌 Added ID strategy: {element_id}")

            # Handle data-* attributes
            for attr, value in attributes.items():
                if attr.startswith('data-'):
                    # CSS Selector using data attribute
                    data_attr_selector = f'[{attr}="{value}"]'
                    strategies.append((By.CSS_SELECTOR, data_attr_selector))
                    print(f"📌 Added CSS Selector strategy based on {attr}: {data_attr_selector}")
                    # XPath using data attribute
                    xpath_data_attr = f"//{tag}[@{attr}='{value}']"
                    strategies.append((By.XPATH, xpath_data_attr))
                    print(f"📌 Added XPath strategy based on {attr}: {xpath_data_attr}")

            # If classes are present, build a CSS selector
            if classes:
                # Use only unique class names to reduce the length of the selector
                class_selector = "." + ".".join(classes)
                strategies.append((By.CSS_SELECTOR, f"{tag}{class_selector}"))
                print(f"📌 Added Class-based CSS Selector strategy: {tag}{class_selector}")

            # Build XPath based on text content if it's not too long
            if text and len(text) < 50:  # Avoid using very long texts
                xpath_text = f"//{tag}[contains(., '{text}')]"
                strategies.append((By.XPATH, xpath_text))
                print(f"📌 Added XPath strategy based on text: {xpath_text}")

            # Add attribute-based XPath strategies
            for attr, value in attributes.items():
                if attr not in ['id', 'class', 'text'] and not attr.startswith('data-'):
                    # Handle attributes with quotes in their values
                    if isinstance(value, list):
                        value = ' '.join(value)
                    xpath_attr = f"//{tag}[@{attr}='{value}']"
                    strategies.append((By.XPATH, xpath_attr))
                    print(f"📌 Added XPath strategy based on attribute {attr}: {xpath_attr}")

    # Remove duplicate strategies while preserving order
    seen = set()
    unique_strategies = []
    for method, pattern in strategies:
        if (method, pattern) not in seen:
            unique_strategies.append((method, pattern))
            seen.add((method, pattern))

    print("🔄 Compiled all unique locator strategies.")
    return unique_strategies


def find_and_click(driver, outer_html=None, full_xpath=None, selector=None, js_path=None, iframe_selector=None,
                   timeout=3):
    """
    Locate an element using multiple strategies and click it.

    Parameters:
    - driver: Selenium WebDriver instance.
    - outer_html: The outer HTML of the target element (string).
    - full_xpath: Full XPath of the element.
    - selector: CSS selector of the element.
    - js_path: JavaScript code to execute for clicking the element.
    - iframe_selector: CSS selector or XPath of the iframe containing the target element.
    - timeout: Maximum time to wait for the element to become interactable.

    Returns:
    - True if the click was successful using any method, False otherwise.
    """
    try:
        print("🔍 Starting the element search process...")

        # Switch to iframe if provided
        if iframe_selector:
            try:
                print(f"🔄 Switching to iframe: {iframe_selector}")
                if iframe_selector.startswith(("/", ".")):
                    # Assuming CSS selector
                    iframe = WebDriverWait(driver, timeout).until(
                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, iframe_selector))
                    )
                else:
                    # Assuming XPath
                    iframe = WebDriverWait(driver, timeout).until(
                        EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_selector))
                    )
                print("✅ Switched to iframe successfully.")
            except TimeoutException as e:
                print(f"❌ Failed to switch to iframe: {e}")
                return False

        # Generate locator strategies
        strategies = generate_locator_strategies(outer_html, full_xpath, selector)

        next_button = None

        # Attempt to find the element using the compiled strategies
        for by_method, pattern in strategies:
            try:
                print(f"🔧 Trying to find element by {by_method} with pattern: {pattern}")
                wait = WebDriverWait(driver, timeout)
                element = wait.until(EC.element_to_be_clickable((by_method, pattern)))
                if element.is_displayed():
                    print(f"✅ Element found using {by_method} with pattern: {pattern}")
                    next_button = element
                    break
            except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
                print(f"❌ Failed to find element using {by_method} with pattern: {pattern}. Error: {e}")
                continue

        # If found, attempt to click using different methods
        if next_button:
            # Standard click
            try:
                print("🖱️ Attempting standard click.")
                next_button.click()
                print("✅ Element clicked successfully with standard click!")
                time.sleep(0.88)
                return True
            except (ElementNotInteractableException, ElementClickInterceptedException) as e:
                print(f"❌ Standard click failed: {e}")

            # Scroll into view and click using JavaScript
            try:
                print("📜 Attempting JavaScript click.")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                print("✅ Element clicked successfully with JavaScript!")
                time.sleep(0.88)
                return True
            except Exception as e:
                print(f"❌ JavaScript click failed: {e}")

            # Use ActionChains to move to element and click
            try:
                print("🔄 Attempting ActionChains click.")
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                print("✅ Element clicked successfully with ActionChains!")
                time.sleep(0.88)
                return True
            except Exception as e:
                print(f"❌ ActionChains click failed: {e}")

            # Send ENTER key
            try:
                print("⌨️ Attempting to send ENTER key.")
                next_button.send_keys(Keys.ENTER)
                print("✅ Element clicked successfully by sending ENTER key!")
                time.sleep(0.88)
                return True
            except Exception as e:
                print(f"❌ Sending ENTER key failed: {e}")

        # Fallback: Use JavaScript path if provided
        if js_path:
            try:
                print(f"📜 Attempting to click using JavaScript path: {js_path}")
                driver.execute_script(js_path + ".click();")  # Ensure click() is called
                print("✅ JavaScript executed successfully!")
                time.sleep(0.88)
                return True
            except Exception as e:
                print(f"❌ JavaScript click failed: {e}")

        print("⚠️ Element could not be found or clicked with the provided strategies.")
        return False

    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")
        return False


# Example Usage
if __name__ == "__main__":
    from selenium import webdriver
    import time

    # Initialize the WebDriver (example with Chrome)
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

    try:
        # Navigate to the target page
        driver.get("https://your-target-website.com")  # Replace with your actual URL

        # Optionally, wait for the page to load completely
        time.sleep(3)  # Adjust the sleep time as necessary

        # Example inputs copied from Chrome's inspect element
        outer_html_example = '''
        <button class="btn relative btn-primary btn-small" as="button" data-testid="mobile-login-button">
            <div class="flex items-center justify-center">Log in</div>
        </button>
        '''
        full_xpath_example = "/html/body/div[1]/div[1]/div[1]/div[3]/button"
        selector_example = "body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > div.draggable.sticky.top-0.z-10.flex.min-h-\\[60px\\].items-center.justify-center.border-transparent.bg-token-main-surface-primary.pl-0.md\\:hidden > div.no-draggable.absolute.bottom-0.right-0.top-0.mr-3.inline-flex.items-center.justify-center > button"
        js_path_example = 'document.querySelector("body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > div.draggable.sticky.top-0.z-10.flex.min-h-\\\\[60px\\\\].items-center.justify-center.border-transparent.bg-token-main-surface-primary.pl-0.md\\\\:hidden > div.no-draggable.absolute.bottom-0.right-0.top-0.mr-3.inline-flex.items-center.justify-center > button")'
        iframe_selector_example = None  # Replace with your iframe selector if needed

        # Call the find_and_click function with the provided paths
        success = find_and_click(
            driver=driver,
            outer_html=outer_html_example,
            full_xpath=full_xpath_example,
            selector=selector_example,
            js_path=js_path_example,
            iframe_selector=iframe_selector_example
        )

        if success:
            print("🔗 Click action was successful!")
        else:
            print("❌ Click action failed.")

        # Continue with the rest of your script
        # ...

    finally:
        # Close the driver after all actions
        driver.quit()
