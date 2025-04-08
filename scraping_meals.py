import requests
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

LOGIN_URL = "https://mysu.sabanciuniv.edu/"

def login_and_get_cookies():
    driver = webdriver.Safari()
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys("sipahibasar")
    driver.find_element(By.ID, "password").send_keys("41X41basar.")
    driver.find_element(By.NAME, "submit").click()

    # Wait for any post-login element
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "block-mysu-theme-shuttle")))

    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def apply_cookies_to_session(cookies):
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    return session

def fetch_meals_for_date(session, date_str):
    url = f"https://mysu.sabanciuniv.edu/mysu-bundle/meals/json?date={date_str}"
    response = session.get(url)
    try:
        data = response.json().get("data", [])
        return data
    except Exception as e:
        print(f"❌ Error parsing {date_str}: {e}")
        return []

def get_all_april_meals(session):
    meals_list = []
    current_date = datetime(2025, 4, 1)
    while current_date.month == 4:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"📆 Fetching: {date_str}")
        meals = fetch_meals_for_date(session, date_str)

        for meal in meals:
            meals_list.append({
                "Date": meal.get("tarih", ""),
                "Name": meal.get("name", ""),
                "Category": meal.get("category", ""),
                "Calories": meal.get("calori", ""),
                "Calorie Type": meal.get("calori_arr", {}).get("type", ""),
                "Lunch": meal.get("lunch", False),
                "Dinner": meal.get("dinner", False),
            })

        current_date += timedelta(days=1)
    return meals_list

def export_to_csv(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"✅ Saved to {path}")

def main():
    cookies = login_and_get_cookies()
    session = apply_cookies_to_session(cookies)
    meals = get_all_april_meals(session)
    export_to_csv(meals, "/Users/basarsipahi/Documents/GitHub/MySu-Chatbot/Web Application/Web Scraping/Data/april_meals_2025.csv")

if __name__ == "__main__":
    main()
