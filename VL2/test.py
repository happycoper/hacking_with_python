import json
import subprocess
import tempfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


REPOSITORIES = [
    "https://github.com/OWNER/REPOSITORY",
    "https://github.com/OWNER/REPOSITORY2",
]

SEARCH_TERM = "kirschkuchen"

# Dateien, die durchsucht werden sollen
TEXT_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml",
    ".js", ".html", ".css", ".java", ".c", ".cpp"
}


def search_repository(repo_path):
    hits = []

    for file_path in repo_path.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            lines = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines()
        except OSError:
            continue

        for line_number, line in enumerate(lines, start=1):
            if SEARCH_TERM.lower() in line.lower():
                relative_path = file_path.relative_to(repo_path)

                hits.append({
                    "file": relative_path,
                    "line": line_number,
                    "content": line.strip()
                })

    return hits


def run_bandit(repo_path):
    result = subprocess.run(
        [
            "bandit",
            "-r",
            str(repo_path),
            "-f",
            "json",
            "-q"
        ],
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return []

    try:
        report = json.loads(result.stdout)
        return report.get("results", [])
    except json.JSONDecodeError:
        return []


def main():
    driver = webdriver.Chrome()

    total_hits = 0
    total_bandit_findings = 0

    with tempfile.TemporaryDirectory() as temp_directory:
        temp_path = Path(temp_directory)

        for repo_url in REPOSITORIES:
            repo_name = repo_url.rstrip("/").split("/")[-1]
            repo_path = temp_path / repo_name

            print(f"\n{'=' * 60}")
            print(f"Repository: {repo_url}")
            print("=" * 60)

            try:
                # Repository mit Selenium öffnen
                driver.get(repo_url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "body")
                    )
                )

                # Repository temporär klonen
                clone_result = subprocess.run(
                    [
                        "git",
                        "clone",
                        "--depth",
                        "1",
                        repo_url,
                        str(repo_path)
                    ],
                    capture_output=True,
                    text=True
                )

                if clone_result.returncode != 0:
                    print("Repository konnte nicht geklont werden.")
                    print(clone_result.stderr)
                    continue

                # Nach kirschkuchen suchen
                hits = search_repository(repo_path)

                for hit in hits:
                    print("\nKirschkuchen-Treffer:")
                    print(f"Datei:  {hit['file']}")
                    print(f"Zeile:  {hit['line']}")
                    print(f"Inhalt: {hit['content']}")

                # Bandit ausführen
                bandit_findings = run_bandit(repo_path)

                for finding in bandit_findings:
                    file_name = Path(
                        finding["filename"]
                    ).relative_to(repo_path)

                    print("\nBandit-Fund:")
                    print(f"Test:    {finding['test_id']}")
                    print(f"Datei:   {file_name}")
                    print(f"Zeile:   {finding['line_number']}")
                    print(f"Risiko:  {finding['issue_severity']}")
                    print(f"Meldung: {finding['issue_text']}")

                total_hits += len(hits)
                total_bandit_findings += len(bandit_findings)

                print("\nRepository-Zusammenfassung:")
                print(f"Kirschkuchen-Treffer: {len(hits)}")
                print(f"Bandit-Funde:         {len(bandit_findings)}")

            except Exception as error:
                print(f"Fehler: {error}")

    driver.quit()

    print(f"\n{'=' * 60}")
    print("GESAMTZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Untersuchte Repositorys: {len(REPOSITORIES)}")
    print(f"Kirschkuchen-Treffer:    {total_hits}")
    print(f"Bandit-Funde:            {total_bandit_findings}")


if __name__ == "__main__":
    main()