"""
Headful details scraper using Chrome DevTools Protocol (CDP)

- Reads input URLs from csv_output/results.csv
- Visits each item URL and extracts fields using selectors in nursery_fields.txt
- Appends one row per item to csv_output/details.csv
- Safe to resume; skips URLs already present in details.csv
"""

from playwright.sync_api import sync_playwright
import csv
import os
from typing import Dict, List, Set


RESULTS_CSV = "csv_output/results.csv"
DETAILS_CSV = "csv_output/details.csv"
SELECTORS_FILE = "nursery_fields.txt"


def read_selectors(path: str) -> Dict[str, str]:
    selectors: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            field, selector = line.split(":", 1)
            selectors[field.strip()] = selector.strip()
    return selectors


def read_results(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def ensure_details_csv(path: str, fieldnames: List[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["area", "item_url", *fieldnames])
            writer.writeheader()


def read_done_urls(path: str) -> Set[str]:
    if not os.path.exists(path):
        return set()
    done: Set[str] = set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            done.add(row.get("item_url", ""))
    return done


def extract_fields_from_page(page, selectors: Dict[str, str]) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for field, selector in selectors.items():
        node = page.query_selector(selector)
        if node is None:
            data[field] = ""
            continue
        text = (node.text_content() or "").strip()
        # Normalize whitespace
        data[field] = " ".join(text.split())
    return data


def append_detail_row(path: str, fieldnames: List[str], area: str, url: str, data: Dict[str, str]) -> None:
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["area", "item_url", *fieldnames])
        row = {"area": area, "item_url": url}
        row.update({k: data.get(k, "") for k in fieldnames})
        writer.writerow(row)


def main():
    selectors = read_selectors(SELECTORS_FILE)
    fieldnames = list(selectors.keys())
    ensure_details_csv(DETAILS_CSV, fieldnames)
    done = read_done_urls(DETAILS_CSV)
    results = read_results(RESULTS_CSV)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        if not browser.contexts:
            browser.close()
            raise RuntimeError("No browser contexts available. Please launch Chrome with remote debugging.")
        context = browser.contexts[0]
        page = context.new_page()
        try:
            for row in results:
                area = row.get("area", "")
                url = row.get("item_url", "")
                if not url or url in done:
                    continue
                print(f"Scraping details: {url}")
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2000)
                data = extract_fields_from_page(page, selectors)
                append_detail_row(DETAILS_CSV, fieldnames, area, url, data)
        finally:
            page.close()


if __name__ == "__main__":
    main()


