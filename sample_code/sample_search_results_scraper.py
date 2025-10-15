"""
Headful search results scraper using Chrome DevTools Protocol (CDP)

- Builds search URLs for given areas (London, Birmingham)
- Paginates until 50 items per area or no more results
- Appends rows incrementally to csv_output/results.csv
- Columns: area, title, item_url, results_page_url
"""

from playwright.sync_api import sync_playwright
import csv
import os
from typing import Iterable, Tuple


AREAS = [
    ("London", "https://www.daynurseries.co.uk/day_nursery_search_results.cfm/searchcounty/London/startpage/{page}"),
    ("Birmingham", "https://www.daynurseries.co.uk/day_nursery_search_results.cfm/searchunitary/Birmingham/startpage/{page}"),
]

MAX_PER_AREA = 50
OUTPUT = "csv_output/results.csv"


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


def parse_results_on_page(page) -> Iterable[Tuple[str, str]]:
    # Each search result card appears under a container with class "sr"
    cards = page.query_selector_all(".sr")
    for card in cards:
        link = card.query_selector("header a[title][href]")
        if not link:
            continue
        title = (link.get_attribute("title") or link.inner_text()).strip()
        href = link.get_attribute("href") or ""
        if not href:
            continue
        yield title, href


def scrape_area(context, area_name: str, url_template: str) -> int:
    collected = 0
    page_num = 1
    page = context.new_page()
    try:
        while collected < MAX_PER_AREA:
            url = url_template.format(page=page_num)
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            items = list(parse_results_on_page(page))
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
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        if not browser.contexts:
            browser.close()
            raise RuntimeError("No browser contexts available. Please launch Chrome with remote debugging.")
        context = browser.contexts[0]

        total = 0
        for area_name, url_template in AREAS:
            print(f"Scraping area: {area_name}")
            count = scrape_area(context, area_name, url_template)
            print(f"Collected {count} items for {area_name}")
            total += count

        print(f"Done. Total items collected: {total}. Saved to {OUTPUT}")


if __name__ == "__main__":
    main()


