import csv
from lxml import html


def read_selectors(path: str) -> dict:
    selectors: dict[str, str] = {}
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


def extract_fields(html_path: str, selectors: dict) -> dict:
    with open(html_path, "r", encoding="utf-8") as f:
        doc = html.fromstring(f.read())
    data: dict[str, str] = {}
    for field, xpath_expr in selectors.items():
        nodes = doc.xpath(xpath_expr)
        if not nodes:
            data[field] = ""
            continue
        node = nodes[0]
        # node can be element or string; use text_content when available
        try:
            text = node.text_content()
        except AttributeError:
            text = str(node)
        text = " ".join((text or "").split())
        data[field] = text
    return data


if __name__ == "__main__":
    selectors = read_selectors("sample_scripts/selectors.txt")
    data = extract_fields(
        "html_input/Bright Horizons nursery.html",
        selectors,
    )
    # Print to console and write a CSV for quick inspection
    print("Extracted fields:")
    for k, v in data.items():
        print(f"- {k}: {v}")

    with open("csv_output/test_details_extract.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(selectors.keys()))
        writer.writeheader()
        writer.writerow(data)


