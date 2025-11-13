import sys

import requests
from bs4 import BeautifulSoup as BS


def main():
    if len(sys.argv) < 2:
        print("Usage: python first_p_test.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BS(requests.get(url, headers=headers, timeout=30).text, "lxml")
    paragraph = soup.select_one("p")
    print(soup.prettify()[:500])
    print("First <p> text:", paragraph.get_text(strip=True) if paragraph else "")

if __name__ == "__main__":
    main()