"""
Headful search results scraper using Chrome DevTools Protocol (CDP)

- Builds search URLs for given areas (London, Birmingham)
- Paginates until 50 items per area or no more results
- Appends rows incrementally to csv_output/results.csv
- Columns: area, title, item_url, results_page_url
"""

import csv
import json
import os
from typing import Iterable, Tuple
from playwright.sync_api import sync_playwright


AREAS = [
    ("London", "https://www.daynurseries.co.uk/day_nursery_search_results.cfm/searchcounty/London/startpage/{page}"),
    ("Birmingham", "https://www.daynurseries.co.uk/day_nursery_search_results.cfm/searchunitary/Birmingham/startpage/{page}"),
]

MAX_PER_AREA = 50
OUTPUT = "csv_output/results.csv"
SELECTORS_FILE = "results_fields_validated.json"


def ensure_csv(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["area", "title", "item_url", "results_page_url"])
            writer.writeheader()


def append_rows(path: str, rows: Iterable[dict]) -> None:
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["area", "title", "item_url", "results_page_url"])
        for row in rows:
            writer.writerow(row)


def load_selectors(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    required_keys = {"item_selector", "item_title", "item_url"}
    missing = required_keys.difference(data.keys())
    if missing:
        raise ValueError(f"Missing selector keys: {', '.join(sorted(missing))}")
    return data


def parse_results_on_page(page, selectors: dict) -> Iterable[Tuple[str, str]]:
    cards = page.query_selector_all(selectors["item_selector"])
    for card in cards:
        link = card.query_selector(selectors["item_title"])
        if not link:
            continue
        title = (link.inner_text() or "").strip()
        href_attr = selectors["item_url"]
        href_node = card.query_selector(href_attr)
        href = href_node.get_attribute("href") if href_node else ""
        if not href:
            continue
        yield title, href


def scrape_area(context, area_name: str, url_template: str, selectors: dict) -> int:
    collected = 0
    page_num = 1
    page = context.new_page()
    try:
        while collected < MAX_PER_AREA:
            url = url_template.format(page=page_num)
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            items = list(parse_results_on_page(page, selectors))
            if not items:
                break

            # Trim to remaining budget
            remaining = MAX_PER_AREA - collected
            items = items[:remaining]

            append_rows(
                OUTPUT,
                ({
                    "area": area_name,
                    "title": title,
                    "item_url": href,
                    "results_page_url": url,
                } for title, href in items)
            )

            collected += len(items)
            page_num += 1
    finally:
        page.close()
    return collected


def main():
    ensure_csv(OUTPUT)
    selectors = load_selectors(SELECTORS_FILE)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        if not browser.contexts:
            browser.close()
            raise RuntimeError("No browser contexts available. Please launch Chrome with remote debugging.")
        context = browser.contexts[0]

        total = 0
        for area_name, url_template in AREAS:
            print(f"Scraping area: {area_name}")
            count = scrape_area(context, area_name, url_template, selectors)
            print(f"Collected {count} items for {area_name}")
            total += count

        print(f"Done. Total items collected: {total}. Saved to {OUTPUT}")


if __name__ == "__main__":
    main()


