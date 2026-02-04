import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLIENT_URL = os.getenv("CLIENT", "http://localhost:3000")

def click_calendar(data: dict):
    date = data["date"]
    hour = data["hour"]
    candidate_name = data.get("name") or "Unknown Candidate"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 40)

    try:
        url = f"{CLIENT_URL}/calendar"
        print("→ Opening:", url)
        driver.get(url)

        driver.execute_script(
            "localStorage.setItem('candidate_name', arguments[0]);",
            candidate_name
        )

        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid")))

        wait.until(EC.element_to_be_clickable((By.ID, f"date-{date}"))).click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal")))

        wait.until(EC.element_to_be_clickable((By.ID, f"slot-{date}-{hour}"))).click()

        swal_ok = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", swal_ok)
        time.sleep(0.5)
        swal_ok.click()

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()