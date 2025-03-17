from selenium import webdriver  # Import Selenium WebDriver to control the browser
import time  # Import time module for delays
from selenium.webdriver.common.by import By  # Import By for element selection
from selenium.webdriver.chrome.service import Service
import os
import sys

# Locate chromedriver.exe inside the extracted folder
if getattr(sys, 'frozen', False):  # If running as an executable
    driver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
else:
    driver_path = "chromedriver.exe"  # Normal case for script execution

# Set up Chrome WebDriver properly
chrome_options = webdriver.ChromeOptions()
service = Service(driver_path)  # Use Service() to specify chromedriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Cookie Clicker game
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Find the cookie element to click on
cookie = driver.find_element(By.ID, "cookie")

# Get all upgrade items available in the store
items = driver.find_elements(By.CSS_SELECTOR, "#store div")

# Extract and store the item IDs of the upgrade options
item_ids = [item.get_attribute("id") for item in items]

# Set initial timeouts
timeout = time.time() + 5  # Next upgrade check in 5 seconds
five_min = time.time() + 60 * 5  # Stop bot after 5 minutes

# Main bot loop
while True:
    # Click the cookie repeatedly
    cookie.click()

    # Every 5 seconds, check for available upgrades
    if time.time() > timeout:

        # Get all upgrade items' price elements (inside <b> tags)
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Extract and convert the upgrade prices to integers
        for price in all_prices:
            element_text = price.text
            if element_text != "":  # Ensure it's not empty
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create a dictionary of store items with their prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get the current number of cookies available
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:  # Remove commas for easier conversion
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)
        print(f"Current amount of money: {cookie_count}")

        # Identify upgrades that can be afforded
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:  # If we have enough cookies, store the upgrade
                affordable_upgrades[cost] = id
                print(f"Upgrade we can afford: {id} @ {cost}")

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)  # Get the most expensive item we can buy
        print(f"Purchasing most expensive upgrade: {affordable_upgrades[highest_price_affordable_upgrade]} @ {highest_price_affordable_upgrade}")  # Debugging output

        # Click to purchase the selected upgrade
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        driver.find_element(By.ID, to_purchase_id).click()

        # Reset the timeout for the next upgrade check
        timeout = time.time() + 5

    # Stop the bot after 5 minutes and display the cookies per second (CPS) rate
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text  # Get cookies per second rate
        print("After 5 minutes, your cookies per second = ", cookie_per_s)  # Output CPS to console
        break  # Exit the loop and stop the bot
