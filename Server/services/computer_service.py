import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CLIENT_URL = os.getenv("CLIENT", "http://localhost:3000")

def click_calendar(data: dict):
    date = data["date"]
    hour = data["hour"]

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    url = f"{CLIENT_URL}/calendar"
    driver.get(url)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid")))

    wait.until(EC.element_to_be_clickable((By.ID, f"date-{date}"))).click()

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal")))

    wait.until(EC.element_to_be_clickable((By.ID, f"slot-{date}-{hour}"))).click()

    swal_ok = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
    )
    swal_ok.click()

    driver.quit()
    return {"status": "success"}