from selenium.common import NoSuchElementException

from step2_MariaDB_database_engine import query_database
import random
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker


def query_production_table_for_usernames(no_of_usernames=1):
    # Fetch random record from production table
    # Excluding "_" from name and setting length limit to >+ 6, as per Gmail Rules.
    query = (f"SELECT username FROM high_probability_real_usernames "
             f"WHERE username NOT LIKE '%\\_%' AND LENGTH(username) >= 6 "
             f"ORDER BY RAND() "
             f"LIMIT {no_of_usernames};")
    query_results = query_database(query)
    print(query_results)
    genesis_usernames = None
    # Check if query_results is not empty
    if query_results:
        # Extract usernames (assuming query_results is a list of dictionaries)
        genesis_usernames = [result['username'] for result in query_results]
        print(f"Usernames we'll be checking Gmail validity for: {genesis_usernames}")
    else:
        print("No usernames found in the database.")

    return genesis_usernames


def send_keys(element, text, min_delay=0.07, max_delay=0.33):
    """Send keys to an element one character at a time with random delays."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay * unit_of_measurement, max_delay * unit_of_measurement))


def init_browser():
    """Initialize and return a Chrome browser instance."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver


def open_signup_page(driver):
    """Navigate to the Google Account signup page."""
    driver.get("https://accounts.google.com/signup")
    time.sleep(1.3 * unit_of_measurement)


def enter_name(driver):
    # Initialize the Faker instance
    fake = Faker()
    """Enter first and last name into the signup form."""
    # Generate random first and last name using Faker
    first_name = fake.first_name()
    last_name = fake.last_name()
    # Print values for debugging purposes
    print(f"Generated name: {first_name} {last_name}")

    firstname_input = driver.find_element(By.ID, 'firstName')
    lastname_input = driver.find_element(By.ID, 'lastName')
    send_keys(firstname_input, first_name)
    time.sleep(0.7 * unit_of_measurement)
    send_keys(lastname_input, last_name)
    time.sleep(0.7 * unit_of_measurement)


def click_next(driver, by_method, selector):
    """Click the 'Next' button on the form."""
    if by_method == 'css':
        next_button = driver.find_element(By.CSS_SELECTOR, selector)
    elif by_method == 'xpath':
        next_button = driver.find_element(By.XPATH, selector)
    else:
        raise ValueError("Invalid by_method")
    next_button.click()
    time.sleep(0.88 * unit_of_measurement)


def enter_birthdate_and_gender(driver):
    """Enter birthdate and select gender."""
    # Generate random month (1-12)
    month = str(random.randint(1, 12))

    # Generate random day (1-28 to ensure valid day for all months)
    day = str(random.randint(1, 28))

    # Generate random year between 1950 and 2010
    year = str(random.randint(1950, 2010))

    # Generate random gender ('1' for male, '2' for female, '3' for others)
    gender = str(random.choice(['1', '2', '3']))

    month_dropdown = driver.find_element(By.ID, 'month')
    month_dropdown.click()
    time.sleep(1 * unit_of_measurement)
    month_option = driver.find_element(By.XPATH, f"//option[@value='{month}']")
    month_option.click()
    time.sleep(1 * unit_of_measurement)
    day_input = driver.find_element(By.ID, 'day')
    send_keys(day_input, str(day))
    time.sleep(1 * unit_of_measurement)
    year_input = driver.find_element(By.ID, 'year')
    send_keys(year_input, str(year))
    time.sleep(1 * unit_of_measurement)
    gender_dropdown = driver.find_element(By.ID, 'gender')
    driver.execute_script(f"arguments[0].value = '{gender}';", gender_dropdown)
    time.sleep(0.5 * unit_of_measurement)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", gender_dropdown)
    time.sleep(1 * unit_of_measurement)


def create_new_address(driver, username):
    # Create New Gmail Address
    radio_button = driver.find_element(By.XPATH, "//div[@role='radio' and @data-value='1']")
    # Click the radio button
    ActionChains(driver).move_to_element(radio_button).click().perform()
    time.sleep(0.5 * unit_of_measurement)
    # Click the next button again
    click_next(driver, 'xpath', "//span[text()='Next']")
    time.sleep(0.5 * unit_of_measurement)

    ######################################################################################################
    # Google Anti_WebScraping detected - generating multiple and different pages and cannot find element #
    ######################################################################################################
    # 1st Path: Create your Own Gmail Address Path (not always triggered)
    try:
        radio_button_2 = driver.find_element(By.XPATH,
                                             "//div[@role='radio' and @data-value='custom' and @aria-posinset='3']")
        # Click the custom radio button
        ActionChains(driver).move_to_element(radio_button_2).click().perform()
        time.sleep(0.5 * unit_of_measurement)
    except NoSuchElementException:
        # If the radio button is not found, skip this step and continue
        print("Custom radio button not found, moving on to next step.")

    # 2nd Path: Fill in the username in either of the two potential input fields
    try:
        # Try the first possible input field for the username
        username_input = driver.find_element(By.XPATH,
                                             "//input[@name='Username' and @aria-label='Create a Gmail address']")
        # Paste the processed_username into the field
        username_input.clear()
        username_input.send_keys(username)
        print(f"Username filled in using the first input field: {username}")

    except NoSuchElementException:
        # If the first input field isn't found, try the second possible input field
        try:
            # Locate the alternative input field for the username
            username_input_alt = driver.find_element(By.XPATH, "//input[@name='Username' and @aria-label='Username']")
            # Paste the processed_username into the alternative field
            username_input_alt.clear()
            username_input_alt.send_keys(username)
            print(f"Username filled in using the alternative input field: {username}")

        except NoSuchElementException:
            # If neither field is found, handle it accordingly
            print("Neither of the username input fields was found. Skipping this step.")

    # Finally Click Next Button - if Error -> Email validated & exists.
    click_next(driver, 'xpath', "//span[text()='Next']")
    time.sleep(2 * unit_of_measurement)


def handle_username_availability(driver):
    try:
        # Look for the message "That username is taken."
        username_taken_element = driver.find_element(By.XPATH, "//div[contains(text(), 'That username is taken')]")

        # If the element is found, print the message that the username is taken
        print("The username is taken. The email is valid & used.")
        return False

    except NoSuchElementException:
        # If the element is not found, assume the username is available
        print("The username is available.")
        return True


def process_username(driver, processed_username):
    """
    Function to process each username and check availability.
    """
    open_signup_page(driver)
    enter_name(driver)
    click_next(driver, 'css', '#collectNameNext > div > button > span')
    enter_birthdate_and_gender(driver)
    click_next(driver, 'xpath', "//span[text()='Next']")
    create_new_address(driver, processed_username)

    # Handle username existing or not
    availability = handle_username_availability(driver)

    # Return the formatted result
    return f"{processed_username}@gmail.com {'available' if availability else 'not available'}"


# Randomize unit_of_measurement
unit_of_measurement = random.uniform(0.58, 0.85)
# User Flags
number_of_processed_records = 2
# Pace Coeficient - controls the time between interactions
pace_coefficient = 0.8
unit_of_measurement = unit_of_measurement * pace_coefficient


def main():
    # Initiate Usernames to Validate
    processed_usernames = query_production_table_for_usernames(2)

    # Initialize browser
    driver = init_browser()

    # Store results
    username_results = []

    # Loop through all the usernames and process each
    for processed_username in processed_usernames:
        result = process_username(driver, processed_username)
        username_results.append(result)

        # Optionally, add a delay between processing usernames if necessary
        time.sleep(2)  # Adjust or remove this delay as needed

    # Print all results at the end
    print("\n Results:")
    print("\n".join(username_results))

    # Close the browser after processing all usernames
    driver.quit()


if __name__ == "__main__":
    main()
