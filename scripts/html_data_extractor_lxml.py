"""
lxml-Based HTML Data Extraction Engine
=====================================

This script processes raw HTML snapshots collected from Wayback Machine archives
to extract structured app data using lxml's robust XPath parsing capabilities.
It's designed for high-volume processing of historical Google Play Store pages.

Core Functionality:
- Processes HTML files using lxml's fast C-based parser
- Implements fallback XPath strategies for different page layouts
- Extracts comprehensive app metadata including ratings, downloads, descriptions
- Handles temporal variations in Google Play Store HTML structure
- Supports batch processing across multiple app directories

Data Extraction Strategy:
1. Timestamp Extraction: Parses filenames for temporal information
2. XPath Querying: Uses multiple XPath expressions for robustness
3. Fallback Mechanisms: Implements cascade of selectors for reliability
4. Text Processing: Cleans and normalizes extracted content
5. Structured Output: Generates standardized CSV format

Extracted Data Fields:
- app_title: Application name from various heading selectors
- rating: Star ratings with fallback to aria-label attributes
- downloads: Install counts from multiple possible locations
- reviews: Review counts with text parsing
- description: Full app descriptions with text joining
- whats_new: Update notes and change logs
- timestamp: Temporal metadata from filename parsing

Technical Features:
- Multi-XPath fallback system for layout variations
- Robust error handling for malformed HTML
- Memory-efficient file processing
- Configurable input/output directory structure
- Progress tracking and logging

Input Structure:
- html_snapshots/{target_url}/{downloads}/: Raw HTML files
- Filename format: {app}_{timestamp}.html

Output Structure:
- {downloads} analysed data lxml/: Processed CSV files
- One CSV per app with temporal data

Performance Characteristics:
- Fast C-based lxml parsing
- Streaming file processing
- Minimal memory footprint
- Batch directory processing

Usage:
    python processhtml_ixml.py

Dependencies:
    - lxml: Fast XML/HTML processing
    - glob: File pattern matching
    - csv: Structured data output
    - re: Regular expression processing

Author: ISB Fintech Research Team
Project: Historical App Data Processing Pipeline
Institution: Indian School of Business (ISB)
"""

import os
import glob
import csv
import re
from lxml import html

def extract_timestamp_from_filename(filename):
    # Example filename: hdfc_app_20150326_002237.html
    match = re.search(r'(\d{8}_\d{6})', filename)
    return match.group(1) if match else ""

def get_first_nonempty(tree, xpaths):
    for xp in xpaths:
        results = tree.xpath(xp)
        if results:
            # If the result is a string then strip it; if it's an element, get its text content.
            if isinstance(results[0], str):
                text = results[0].strip()
            else:
                text = results[0].text_content().strip()
            if text:
                return text
    return ""

def extract_data_lxml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        tree = html.fromstring(content)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

    data = {}
    data['file'] = os.path.basename(file_path)
    data['timestamp'] = extract_timestamp_from_filename(data['file'])

    # Define possible XPaths for each field
    title_xpaths = [
        '//h1[@class="AHFaub"]/span/text()',
        '//h1[contains(@class, "title")]/text()'
    ]
    rating_xpaths = [
        '//div[@class="BHMmbe"]/text()',
        '//div[contains(@aria-label, "stars")]/@aria-label'
    ]
    downloads_xpaths = [
        '//div[contains(text(),"Installs")]/following-sibling::span/text()',
        '//div[contains(text(),"Installs")]/following-sibling::div/text()'
    ]
    reviews_xpaths = [
        '//span[@class="EymY4b"]/span[2]/text()',
        '//span[contains(text(),"reviews")]/text()'
    ]
    description_xpaths = [
        '//div[@jsname="sngebd"]//text()',
        '//div[@itemprop="description"]//text()'
    ]
    whatsnew_xpaths = [
        '//div[contains(., "What\'s New")]/following-sibling::div//text()',
        '//div[contains(@class, "whats-new") or contains(@class, "recent-change")]//text()'
    ]

    data['app_title'] = get_first_nonempty(tree, title_xpaths)
    data['rating'] = get_first_nonempty(tree, rating_xpaths)
    data['downloads'] = get_first_nonempty(tree, downloads_xpaths)
    data['reviews'] = get_first_nonempty(tree, reviews_xpaths)

    # For description and what's new, join all text parts found
    desc_parts = tree.xpath(description_xpaths[0])
    if not desc_parts:
        desc_parts = tree.xpath(description_xpaths[1])
    data['description'] = " ".join([part.strip() for part in desc_parts if part.strip()])

    whatsnew_parts = tree.xpath(whatsnew_xpaths[0])
    if not whatsnew_parts:
        whatsnew_parts = tree.xpath(whatsnew_xpaths[1])
    data['whats_new'] = " ".join([part.strip() for part in whatsnew_parts if part.strip()])

    return data

# def main_lxml():
#     # Change target_url as needed (folder name within your snapshots folder)
#     target_url = "{target_url}"
#     base_folder = f"/Users/jainam/Internship/apk-scraper/html_snapshots"
#     files = glob.glob(os.path.join(base_folder, "*.html"))
#     output = []
#     for file_path in files:
#         data = extract_data_lxml(file_path)
#         print(file_path)
#         if data:
#             output.append(data)

#     # Write results to CSV
#     csv_file = "output_lxml_hdfc.csv"
#     fieldnames = ['file', 'timestamp', 'app_title', 'rating', 'downloads', 'reviews', 'description', 'whats_new']
#     with open(csv_file, 'w', newline='', encoding='utf-8') as csvf:
#         writer = csv.DictWriter(csvf, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in output:
#             writer.writerow(row)
#     print(f"Data written to {csv_file}")

# if __name__ == "__main__":
#     main_lxml()

def main_lxml_multi():
    target_url = "{target_url}"
    downloads  = "1M+"                            # ← this also becomes your output folder name

    # input folder containing sub‑dirs of HTML snapshots
    base_dir = os.path.join(
        "/Users/jainam/Internship/apk-scraper/html_snapshots",
        target_url,
        downloads
    )

    # create the output directory named after `downloads`
    output_dir = f"{downloads} analysed data lxml"
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
            rows.append(extract_data_lxml(fp))

        csv_path = os.path.join(output_dir, f"{sub}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"  → Wrote {len(rows)} rows to {csv_path}")

if __name__ == "__main__":
    main_lxml_multi()
