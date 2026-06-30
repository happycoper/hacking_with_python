import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# E:\Programme\Python\python.exe -m pip install bandit
REPOS = [
    "https://github.com/happycoper/hacking_with_python"
    
]

SEARCH_WORD = "password"
HEADLESS = False


def get_repo_data(repo_url):
    parts = urlparse(repo_url).path.strip("/").split("/")

    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    root_url = f"https://github.com/{owner}/{repo}"

    return owner, repo, root_url


def collect_files(driver, repo_url):
    owner, repo, root_url = get_repo_data(repo_url)

    tree_prefix = f"/{owner}/{repo}/tree/"
    blob_prefix = f"/{owner}/{repo}/blob/"

    directories = [root_url]
    visited = set()
    files = set()

    while directories:
        current_url = directories.pop()

        if current_url in visited:
            continue

        visited.add(current_url)

        print(f"[VERZEICHNIS] {current_url}")

        try:
            driver.get(current_url)

            WebDriverWait(driver, 10).until(
                lambda browser: browser.find_element(By.TAG_NAME, "body")
            )

            links = {
                element.get_attribute("href")
                for element in driver.find_elements(
                    By.CSS_SELECTOR,
                    "a[href]"
                )
            }

        except Exception as error:
            print(f"Fehler beim Öffnen: {error}")
            continue

        for link in links:
            if not link:
                continue

            link = link.split("?", 1)[0].split("#", 1)[0]
            path = urlparse(link).path

            if path.startswith(tree_prefix):
                directories.append(link)

            elif path.startswith(blob_prefix):
                files.add(link)

    return owner, repo, root_url, files


def analyze_repo(driver, repo_url, temp_directory):
    owner, repo, root_url, files = collect_files(
        driver,
        repo_url
    )

    repo_directory = Path(temp_directory) / f"{owner}_{repo}"
    repo_directory.mkdir(parents=True, exist_ok=True)

    hits = 0
    python_files = 0

    print(f"\nGefundene Dateien: {len(files)}\n")

    for blob_url in sorted(files):
        try:
            raw_url = blob_url.replace(
                "/blob/",
                "/raw/",
                1
            )

            data = urlopen(
                raw_url,
                timeout=20
            ).read()

            text = data.decode(
                "utf-8",
                errors="ignore"
            )

        except Exception as error:
            print(f"Downloadfehler: {error}")
            continue

        # Branchnamen entfernen und Dateipfad bestimmen
        relative_path = (
            blob_url
            .split("/blob/", 1)[1]
            .split("/", 1)[1]
        )

        # Wortsuche
        for line_number, line in enumerate(
            text.splitlines(),
            start=1
        ):
            if SEARCH_WORD.casefold() in line.casefold():
                hits += 1

                print(
                    f"[TREFFER] {relative_path}:"
                    f"{line_number}: {line.strip()}"
                )

        # Nur Python-Dateien für Bandit speichern
        if relative_path.endswith(".py"):
            target = repo_directory / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")

            python_files += 1

    print("\n" + "=" * 60)
    print(f"Repository:       {root_url}")
    print(f"Dateien:          {len(files)}")
    print(f"Python-Dateien:   {python_files}")
    print(f"Worttreffer:      {hits}")
    print("=" * 60)

    if python_files == 0:
        print("Keine Python-Dateien für Bandit gefunden.")
        return

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            str(repo_directory),
            "-q"
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    print("\n=== BANDIT-ERGEBNIS ===")

    if result.stdout.strip():
        print(result.stdout)
    else:
        print("Keine Bandit-Befunde.")

    if result.stderr.strip():
        print("Bandit-Fehler:")
        print(result.stderr)


def main():
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    try:
        # Wird nach Programmende automatisch gelöscht
        with tempfile.TemporaryDirectory() as temp_directory:
            for repo_url in REPOS:
                print("\n" + "#" * 70)
                print(f"Analysiere: {repo_url}")
                print("#" * 70)

                analyze_repo(
                    driver,
                    repo_url,
                    temp_directory
                )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()