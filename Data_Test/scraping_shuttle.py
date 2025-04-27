import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os

LOGIN_URL = "https://mysu.sabanciuniv.edu/"
SHUTTLE_API_URL = "https://mysu.sabanciuniv.edu/mysu-bundle/shuttle/shuttle-ajax-data"

def login_and_get_cookies():
    driver = webdriver.Safari()
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys("username")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.NAME, "submit").click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "block-mysu-theme-shuttle")))
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def apply_cookies_to_session(cookies):
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session

def fetch_shuttle_data(session):
    response = session.get("https://mysu.sabanciuniv.edu/mysu-bundle/shuttle/shuttle-ajax-data")

    print("✅ Response received. Parsing HTML...")
    soup = BeautifulSoup(response.text, "html.parser")

    all_shuttles = []

    for item in soup.select(".drop-menu-item"):
        try:
            direction = "From Campus" if "from-campus" in item["class"] else "To Campus"
            departure = item.select_one(".date-list-start .table-title").text.strip()
            arrival = item.select_one(".date-list-finish .table-title").text.strip()

            for time_tag in item.select(".closest-content span"):
                time_text = time_tag.text.strip()
                if time_text and "no upcoming ride" not in time_text.lower():
                    all_shuttles.append({
                        "Direction": direction,
                        "Departure": departure,
                        "Arrival": arrival,
                        "Time": time_text
                    })
        except Exception as e:
            print("❌ Error parsing a shuttle block:", e)

    return all_shuttles


def parse_shuttle_data(json_data):
    records = []
    for direction_key in json_data.keys():
        for route in json_data[direction_key]:
            direction = "To Campus" if route.get("is_to_campus") else "From Campus"
            departure = route.get("departure", "")
            arrival = route.get("arrival", "")
            times = route.get("times", [])

            for time_entry in times:
                time = time_entry.get("time", "")
                if time:
                    records.append({
                        "Direction": direction,
                        "Departure": departure,
                        "Arrival": arrival,
                        "Time": time
                    })
    return records



def save_shuttle_schedule(data):
    df = pd.DataFrame(data)
    df.to_csv("/Users/basarsipahi/Documents/GitHub/MySu-Chatbot/Web Application/Web Scraping/Data/shuttle_schedule_tryy.csv", index=False)
    print("📄 Saved to shuttle_schedule.csv")

def main():
    cookies = login_and_get_cookies()
    session = apply_cookies_to_session(cookies)
    
    shuttle_data = fetch_shuttle_data(session)
    save_shuttle_schedule(shuttle_data)




if __name__ == "__main__":
    main()
