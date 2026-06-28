from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re

driver = webdriver.Chrome()

SEARCHFOR = "password"

REPOS = [
    "https://github.com/happycoper/hacking_with_python"
    
]

visited = set()

def scan_files(url):
    try:
        driver.get(url)
        #time.sleep(0.2)

        text = driver.find_element(By.TAG_NAME, "body").text

        pattern = rf"{SEARCHFOR}\s*=\s*[\"'](.*?)[\"']"
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            for m in matches:
                print("\n=== CODE TREFFER ===")
                print(f"Variable: {SEARCHFOR}")
                print(f"Wert: {m}")
                print(f"Link: {url}")


    except Exception as e:
        print("Fehler", e)

def runs(url):
    if url in visited:
        return
    visited.add(url)
    
    try:
        driver.get(url)
        #time.sleep(0.2)

        links = []

        for a in driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")

            if href:
                links.append(href)

        for href in links:
            name = href.rstrip("/").split("/")[-1]
            if SEARCHFOR in name.lower():
                print("\n=== TREFFER IM NAMEN ===")
                print(f"Name: {name}")
                print(f"Link: {href}")

            if "/tree/" in href:
                runs(href)

            elif "/blob/" in href:
                scan_files(href)

    except Exception as e:
        print("Fehler bei", url, e)


for repo in REPOS:
    print(f"\nStarte Repository: {repo}")
    runs(repo)

driver.quit()
