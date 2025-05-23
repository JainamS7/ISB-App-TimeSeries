import os
import glob
import csv
import re
from bs4 import BeautifulSoup

def extract_timestamp_from_filename(filename):
    match = re.search(r'(\d{8}_\d{6})', filename)
    return match.group(1) if match else ""

def get_first_nonempty_bs(soup, selectors):
    for sel in selectors:
        elements = soup.select(sel)
        if elements:
            text = elements[0].get_text(strip=True)
            if text:
                return text
    return ""

def extract_data_bs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    data = {
        'file': os.path.basename(file_path),
        'timestamp': extract_timestamp_from_filename(os.path.basename(file_path)),
        'app_title': get_first_nonempty_bs(soup, ["h1.AHFaub span", "h1.title"]),
        'rating':    get_first_nonempty_bs(soup, ["div.BHMmbe", "div[aria-label*='stars']"]),
        'downloads': get_first_nonempty_bs(soup, ["div:contains('Installs') + span", "div:contains('Installs') + div"]),
        'reviews':   get_first_nonempty_bs(soup, ["span.EymY4b span:nth-of-type(2)", "span:contains('reviews')"])
    }

    desc = soup.select_one("div[jsname='sngebd'], div[itemprop='description']")
    data['description'] = desc.get_text(" ", strip=True) if desc else ""
    wn   = soup.select_one("div:contains(\"What's New\") + div, div.whats-new, div.recent-change")
    data['whats_new'] = wn.get_text(" ", strip=True) if wn else ""
    return data

def main_bs_multi():
    target_url = "{target_url}"
    downloads  = "500M+"                            # ← this also becomes your output folder name

    # input folder containing sub‑dirs of HTML snapshots
    base_dir = os.path.join(
        "/Users/jainam/Internship/apk-scraper/html_snapshots",
        target_url,
        downloads
    )

    # create the output directory named after `downloads`
    output_dir = f"{downloads} analysed data"
    os.makedirs(output_dir, exist_ok=True)

    fieldnames = [
        'file','timestamp','app_title','rating',
        'downloads','reviews','description','whats_new'
    ]

    for sub in os.listdir(base_dir):
        sub_path = os.path.join(base_dir, sub)
        if not os.path.isdir(sub_path):
            continue

        print(f"Processing folder: {sub}")
        rows = []
        for fp in glob.glob(os.path.join(sub_path, "*.html")):
            rows.append(extract_data_bs(fp))

        csv_path = os.path.join(output_dir, f"{sub}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"  → Wrote {len(rows)} rows to {csv_path}")

if __name__ == "__main__":
    main_bs_multi()
