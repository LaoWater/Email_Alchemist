import random
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to send keys letter by letter with a random delay between 0.15 and 0.5 seconds
def send_keys_slowly(element, text, min_delay=0.07, max_delay=0.33):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


# Initialize the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Google Account signup page
driver.get("https://accounts.google.com/signup")

# Maximize the browser window
driver.maximize_window()

# Wait for the page to load fully
time.sleep(2)

# Example: Find the first name and last name input fields
firstname_input = driver.find_element(By.ID, 'firstName')
lastname_input = driver.find_element(By.ID, 'lastName')

# Example: Slowly enter data into the input fields with random delays between keystrokes
send_keys_slowly(firstname_input, 'Dodo')
time.sleep(1)
send_keys_slowly(lastname_input, 'Bartos')
time.sleep(1)

# Find and click the 'Next' button
next_button = driver.find_element(By.CSS_SELECTOR, '#collectNameNext > div > button > span')
next_button.click()

# Wait for the next page to load
time.sleep(1.5)

# Now on the next page, fill in date of birth and gender
# Example: Find the date fields (Month, Day, Year) and Gender selection

# Select birth month (this example selects the month by visible text or value)
month_dropdown = driver.find_element(By.ID, 'month')
month_dropdown.click()
time.sleep(1)
month_option = driver.find_element(By.XPATH, "//option[@value='1']")  # 1 for January
month_option.click()
time.sleep(1)

# Enter day of birth
day_input = driver.find_element(By.ID, 'day')
send_keys_slowly(day_input, '15')
time.sleep(1)

# Enter year of birth
year_input = driver.find_element(By.ID, 'year')
send_keys_slowly(year_input, '1990')
time.sleep(1)

# Select gender using JavaScript (example: selecting 'Male')
gender_dropdown = driver.find_element(By.ID, 'gender')
# Use JavaScript to set the value of the dropdown directly
driver.execute_script("arguments[0].value = '1';", gender_dropdown)  # '1' is for Male
time.sleep(0.5)
# Optionally, trigger a change event to simulate user interaction
driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", gender_dropdown)

# Example: Click the 'Next' button to continue
time.sleep(1)
# Locate the 'Next' button using XPath based on the text inside the <span> tag
next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
print("Found next button, proceeding to click it")
next_button.click()


##################################################
## Google Email-Creating Work-Flow breaks in 2: ##
## 1. Allow sign-up directly -> asking to choose username ##
## or 2. Asking once again to sign in or create new google account ##
## This is Part of Google Web Scraping security, Treating both cases ##
#######################################################################

# Wait for the next page to load
time.sleep(1000)
# Perform any further automation tasks here

# Close the browser
driver.quit()
