from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# URLs
LOGIN_URL = "https://mysu.sabanciuniv.edu/en"
ACADEMIC_CALENDAR_URL = "https://apps.sabanciuniv.edu/custom/academic-calendar/?a=0&b=2024&c=16&d=en&e=0"

# Configure Selenium WebDriver for Safari
driver = webdriver.Safari()

def login():
    """Logs into MySU using Selenium."""
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))

    # Assuming environment variables or fixed values for USERNAME and PASSWORD
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys("username")  # Replace with your username
    password_input.send_keys("password")  # Replace with your password

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "submit"))
    )
    submit_button.click()
    time.sleep(10)  # Wait for the login process to complete

def scrape_academic_calendar():
    """Scrapes the academic calendar data from MySU."""
    driver.get(ACADEMIC_CALENDAR_URL)
    time.sleep(5)  # Wait for the page to fully load

    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all table rows in the calendar table
    rows = soup.find_all('tr')
    
    # Assuming the first row is headers
    headers = [header.text.strip() for header in rows[0].find_all('th')]
    data = []

    # Loop through all rows except the first header row
    for row in rows[1:]:
        cols = [ele.text.strip() for ele in row.find_all('td')]
        data.append(dict(zip(headers, cols)))

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    return df

def main():
    login()
    df = scrape_academic_calendar()
    print(df.head())  # Display the first few rows of the DataFrame

    # Optionally save to CSV
    df.to_csv("/Users/basarsipahi/Documents/GitHub/MySu-Chatbot/Web Application/Web Scraping/Data/academic_calendar.csv", index=False)
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
