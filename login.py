import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def store_session_info(cookies):
    cookies_concatenated = json.dumps({"cookies": cookies})
    with open(os.path.join(os.getcwd(), ".session_info"), "w", encoding="utf-8") as f:
        f.write(cookies_concatenated)


def get_options():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    return options


def check_url_and_store_cookies(driver):
    if driver.current_url == "https://www.linkedin.com/feed/":
        store_session_info(driver.get_cookies())
        return True

    return False


def main():
    email = "testdfdf@gmail.com"
    password = "suportconfg"

    # Initiate Driver
    driver = webdriver.Chrome(options=get_options())
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Fill the details once the page is loaded
    email_elem = driver.find_element(By.ID, "username")
    email_elem.send_keys(email)
    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(password)

    # Submit the login request
    password_elem.submit()

    WebDriverWait(driver, 10).until(check_url_and_store_cookies)


if __name__ == "__main__":
    main()
