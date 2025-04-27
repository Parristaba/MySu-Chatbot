import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

LOGIN_URL = "https://mysu.sabanciuniv.edu/"
ANNOUNCEMENTS_URL = "https://mysu.sabanciuniv.edu/mysu/filter-announcements?page={}"

def login_and_get_cookies():
    driver = webdriver.Safari()
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys("username")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.NAME, "submit").click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "block-mysu-theme-announcements")))
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def apply_cookies_to_session(cookies):
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session
def fetch_announcements(session, max_pages=20):
    all_announcements = []
    for page in range(max_pages):
        url = f"https://mysu.sabanciuniv.edu/mysu/filter-announcements?page={page}"
        response = session.get(url)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            continue

        try:
            json_data = response.json()
            announcements = json_data.get("data", [])
            for item in announcements:
                all_announcements.append({
                    "Title": item.get("title", "").strip(),
                    "Author": item.get("author", "").strip(),
                    "Unit": item.get("author_unit_value", "").strip(),
                    "Created": item.get("created", "").strip(),
                    "Start Date": item.get("start_date", "").strip(),
                    "End Date": item.get("end_date", "").strip(),
                    "Category": item.get("options", "").strip(),
                    "Link": item.get("headline_url", "").strip()
                })
        except Exception as e:
            print(f"⚠️ Error parsing JSON on page {page}: {e}")
            continue
    return all_announcements




def save_announcements_to_csv(data):
    output_dir = "/Users/basarsipahi/Documents/GitHub/MySu-Chatbot/Web Application/Web Scraping/Data"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "announcements.csv")
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"📄 Saved to: {output_path}")


def main():
    cookies = login_and_get_cookies()
    session = apply_cookies_to_session(cookies)
    announcements = fetch_announcements(session, max_pages=5)
    save_announcements_to_csv(announcements)

if __name__ == "__main__":
    main()
