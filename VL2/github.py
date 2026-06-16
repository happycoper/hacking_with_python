from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Repository-URL
REPO_URL = "https://github.com/happycoper/hacking_with_python"

# Suchbegriff
SEARCH_TERM = "password"

driver = webdriver.Chrome()

visited = set()

def search_directory(url):
    if url in visited:
        return

    visited.add(url)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
    except:
        print(f"Fehler beim Laden: {url}")
        return

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows:
        try:
            link = row.find_element(By.CSS_SELECTOR, "a.Link--primary")
            href = link.get_attribute("href")
            name = link.text

            # Verzeichnis
            if "/tree/" in href:
                print(f"[DIR]  {name}")
                search_directory(href)

            # Datei
            elif "/blob/" in href:
                print(f"[FILE] {name}")

                driver.get(href)

                try:
                    code = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "table.highlight")
                        )
                    )

                    if SEARCH_TERM.lower() in code.text.lower():
                        print(f"Treffer gefunden: {href}")

                except:
                    pass

                driver.back()

        except Exception:
            pass

search_directory(REPO_URL)

driver.quit()