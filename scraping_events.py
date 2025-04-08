from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import time
import os

# Set up Selenium
driver = webdriver.Safari()
driver.maximize_window()

def login():
    driver.get("https://mysu.sabanciuniv.edu")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
    
    # Fill in credentials
    driver.find_element(By.ID, "username").send_keys("sipahibasar")
    driver.find_element(By.ID, "password").send_keys("41X41basar.")
    driver.find_element(By.NAME, "submit").click()
    
    # Wait until login is successful (e.g. menu or event block appears)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "events")))

def fetch_events_json():
    driver.get("https://mysu.sabanciuniv.edu/mysu-bundle/events/load?page=0")
    time.sleep(2)

    try:
        json_text = driver.find_element(By.TAG_NAME, "pre").text
    except:
        json_text = driver.find_element(By.TAG_NAME, "body").text

    try:
        json_obj = json.loads(json_text)
        return json_obj.get("data", [])  # ✅ Extract only the event list
    except Exception as e:
        print("❌ JSON parse failed:", e)
        print("Raw response:\n", json_text[:300])
        return []

def export_events_to_csv(events):
    if not events:
        print("⚠️ No events found.")
        return
    df = pd.DataFrame(events)
    df.to_csv("/Users/basarsipahi/Documents/GitHub/MySu-Chatbot/Web Application/Web Scraping/Data/mysu_events.csv", index=False)
    print("✅ Events saved to CSV.")



def main():
    login()
    events = fetch_events_json()
    export_events_to_csv(events)
    driver.quit()

if __name__ == "__main__":
    main()
