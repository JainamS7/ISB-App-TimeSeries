"""
Fintech App Historical Data Collection Script
============================================

This script is a core component of the ISB Fintech App Research Project that collects
historical Google Play Store data using the Wayback Machine. It implements advanced
scraping techniques to gather time-series data for fintech applications.

Key Features:
- Wayback Machine API integration for historical snapshot discovery
- Robust proxy rotation system for distributed scraping
- Adaptive rate limiting and retry mechanisms
- SSL/TLS handling for secure connections
- Comprehensive error handling and logging
- HTML content extraction and storage

Technical Implementation:
- Uses custom TLSAdapter for SSL certificate handling
- Implements proxy rotation using free proxy services
- Applies exponential backoff for failed requests
- Supports batch processing of multiple applications
- Stores raw HTML snapshots for later processing

Data Collection Process:
1. Retrieve available snapshots from Wayback Machine CDX API
2. Filter snapshots by status code and temporal distribution
3. Download HTML content using rotating proxies and headers
4. Extract app metadata using BeautifulSoup parsing
5. Store both raw HTML and structured data

Usage:
    python scrape_html_snapshots.py

Dependencies:
    - requests: HTTP client with session management
    - beautifulsoup4: HTML parsing and data extraction
    - urllib3: SSL/TLS configuration
    - pandas: Data structure management

Author: ISB Fintech Research Team
Project: Comprehensive Fintech App Market Analysis
Institution: Indian School of Business (ISB)
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import csv
import os
from urllib.parse import quote
from requests.exceptions import ConnectionError
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Create a custom TLSAdapter to disable certificate verification
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = ssl.create_default_context()
        # Disable hostname checking and certificate verification
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        pool_kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

# Create a session and mount the adapter for HTTPS connections
session = requests.Session()
session.mount("https://", TLSAdapter())

# User agent and headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

def get_free_proxies():
    """Scrape free HTTPS proxies from free-proxy-list.net"""
    url = "https://free-proxy-list.net/"
    proxies = []
    try:
        # Disable SSL verification here as well
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", id="proxylisttable")
        if table:
            for row in table.tbody.find_all("tr"):
                cols = row.find_all("td")
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                https = cols[6].text.strip()
                if https.lower() == "yes":
                    proxy = f"http://{ip}:{port}"
                    proxies.append(proxy)
    except Exception as e:
        print(f"Error fetching free proxies: {e}")
    return proxies

# Fetch a list of free proxies once and shuffle them
PROXIES = get_free_proxies()
random.shuffle(PROXIES)
if not PROXIES:
    print("Warning: No free proxies found. Requests will be made directly without proxy.")

def get_wayback_snapshots(url):
    """Get all available snapshots from Wayback Machine for a URL"""
    encoded_url = quote(url, safe='')
    cdx_api_url = (
        f"https://web.archive.org/cdx/search/cdx?url={encoded_url}"
        "&output=json&fl=timestamp,original,statuscode,digest,length"
        "&filter=statuscode:200&collapse=timestamp:6"
    )
    
    try:
        response = session.get(cdx_api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            snapshots = response.json()
            # Remove header row if present
            if snapshots and len(snapshots) > 0:
                return snapshots[1:]
            return []
        else:
            print(f"Failed to get snapshots: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting snapshots: {e}")
        return []

def get_snapshot_content(timestamp, url, max_retries=3, base_delay=10):
    """Get the content of a specific snapshot with retry logic and proxy support"""
    wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
    
    for attempt in range(max_retries):
        try:
            delay = base_delay + random.uniform(1, 5)
            print(f"Waiting {delay:.2f} seconds before request...")
            time.sleep(delay)
            
            proxy = None
            if PROXIES:
                proxy_choice = random.choice(PROXIES)
                proxy = {"http": proxy_choice, "https": proxy_choice}
                print(f"Using proxy: {proxy_choice}")
            else:
                print("No proxy being used.")
            
            response = session.get(wayback_url, headers=headers, proxies=proxy, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get snapshot content: {response.status_code}")
                base_delay *= 2  # Increase delay for next attempt
        except ConnectionError as e:
            print(f"Connection error on attempt {attempt+1}/{max_retries}: {e}")
            wait_time = (2 ** attempt) * 60 + random.uniform(1, 30)
            print(f"Waiting {wait_time:.2f} seconds before retrying...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error on attempt {attempt+1}/{max_retries}: {e}")
            wait_time = (2 ** attempt) * 60 + random.uniform(1, 30)
            print(f"Waiting {wait_time:.2f} seconds before retrying...")
            time.sleep(wait_time)
    
    return None

def extract_app_data(html_content):
    """Extract app data from the HTML content"""
    if not html_content:
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    app_data = {}
    
    # App name
    try:
        app_name = soup.select_one('h1[itemprop="name"]')
        if app_name:
            app_data['app_name'] = app_name.text.strip()
        else:
            app_name = soup.select_one('h1.AHFaub')
            if app_name:
                app_data['app_name'] = app_name.text.strip()
            else:
                app_name = soup.select_one('h1')
                if app_name:
                    app_data['app_name'] = app_name.text.strip()
    except Exception as e:
        print(f"Error extracting app name: {e}")
    
    # Developer name
    try:
        developer = soup.select_one('a[itemprop="author"]')
        if developer:
            app_data['developer'] = developer.text.strip()
        else:
            developer = soup.select_one('a.hrTbp')
            if developer:
                app_data['developer'] = developer.text.strip()
    except Exception as e:
        print(f"Error extracting developer: {e}")
    
    # Rating
    try:
        rating = soup.select_one('div.BHMmbe')
        if rating:
            app_data['rating'] = rating.text.strip()
        else:
            rating = soup.select_one('div[itemprop="aggregateRating"] span')
            if rating:
                app_data['rating'] = rating.text.strip()
    except Exception as e:
        print(f"Error extracting rating: {e}")
    
    # Number of reviews
    try:
        reviews = soup.select_one('span[itemprop="ratingCount"]')
        if reviews:
            app_data['reviews'] = reviews.text.strip()
        else:
            reviews = soup.select_one('span.AYi5wd')
            if reviews:
                app_data['reviews'] = reviews.text.strip()
    except Exception as e:
        print(f"Error extracting reviews: {e}")
    
    # Downloads
    try:
        downloads = soup.select_one('span[itemprop="downloadCount"]')
        if downloads:
            app_data['downloads'] = downloads.text.strip()
        else:
            downloads = soup.select_one('span.EymY4b')
            if downloads:
                app_data['downloads'] = downloads.text.strip()
    except Exception as e:
        print(f"Error extracting downloads: {e}")
    
    # Description
    try:
        description = soup.select_one('div[itemprop="description"]')
        if description:
            app_data['description'] = description.text.strip()
        else:
            description = soup.select_one('div.DWPxHb')
            if description:
                app_data['description'] = description.text.strip()
    except Exception as e:
        print(f"Error extracting description: {e}")
    
    # Last updated
    try:
        updated = soup.select_one('div[itemprop="datePublished"]')
        if updated:
            app_data['last_updated'] = updated.text.strip()
        else:
            updated = soup.select_one('span.htlgb')
            if updated:
                app_data['last_updated'] = updated.text.strip()
    except Exception as e:
        print(f"Error extracting last updated: {e}")
    
    # Version
    try:
        version = soup.select_one('div[itemprop="softwareVersion"]')
        if version:
            app_data['version'] = version.text.strip()
        else:
            version_spans = soup.select('span.htlgb')
            for span in version_spans:
                if span.text.strip().startswith('V'):
                    app_data['version'] = span.text.strip()
                    break
    except Exception as e:
        print(f"Error extracting version: {e}")
    
    # Size
    try:
        size = soup.select_one('div[itemprop="fileSize"]')
        if size:
            app_data['size'] = size.text.strip()
    except Exception as e:
        print(f"Error extracting size: {e}")
    
    # Content rating
    try:
        content_rating = soup.select_one('div[itemprop="contentRating"]')
        if content_rating:
            app_data['content_rating'] = content_rating.text.strip()
    except Exception as e:
        print(f"Error extracting content rating: {e}")
    
    # Extract "What's New" field
    try:
        whats_new = soup.select_one('div[itemprop="description"][jsname="sngebd"]')
        if whats_new:
            app_data['whats_new'] = whats_new.text.strip()
        else:
            whats_new = soup.select_one('div.W4P4ne')
            if whats_new:
                app_data['whats_new'] = whats_new.text.strip()
    except Exception as e:
        print(f"Error extracting What's New: {e}")
    
    # Extract full Description
    try:
        description = soup.select_one('div[itemprop="description"][jsname="sngebd"]')
        if description:
            app_data['full_description'] = description.text.strip()
        else:
            description = soup.select_one('div.DWPxHb')
            if description:
                app_data['full_description'] = description.text.strip()
    except Exception as e:
        print(f"Error extracting full description: {e}")
    
    return app_data

def save_html_to_file(app_id, timestamp, html_content):
    """Save the complete HTML content to a text file under a directory named with app_id"""
    html_dir = f"html_snapshots/{app_id}"
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    
    formatted_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y%m%d_%H%M%S')
    filename = f"{html_dir}/{app_id}_{formatted_date}.html"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        return filename
    except Exception as e:
        print(f"Error saving HTML to file: {e}")
        return None

def save_to_csv(app_data, csv_filename, fields):
    """Save a single entry to CSV file"""
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow(app_data)

def process_app(app_id):
    print(f"\nStarting processing for App ID: {app_id}")
    target_url = f"https://play.google.com/store/apps/details?id={app_id}"
    print(f"Target URL: {target_url}")
    
    # Define output filenames and directory for this app
    csv_filename = f"app_data_{app_id}.csv"
    progress_file = f"scraping_progress_{app_id}.txt"
    
    # Check if this app has already been processed (progress file exists)
    if os.path.exists(progress_file):
        print(f"App ID {app_id} has already been processed. Skipping...")
        return
    
    print(f"Fetching snapshots for {target_url}...")
    snapshots = get_wayback_snapshots(target_url)
    print(f"Found {len(snapshots)} snapshots")
    
    fields = [
        'timestamp', 'snapshot_url', 'app_name', 'developer', 'rating', 
        'reviews', 'downloads', 'description', 'last_updated', 
        'version', 'size', 'content_rating', 'whats_new', 'full_description',
        'html_file'
    ]
    
    processed_timestamps = set()
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            processed_timestamps = set(line.strip() for line in f)
    
    for i, snapshot in enumerate(snapshots):
        timestamp = snapshot[0]
        original_url = snapshot[1]
        if timestamp in processed_timestamps:
            print(f"Skipping already processed snapshot {i+1}/{len(snapshots)} from {timestamp}")
            continue
        
        readable_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        print(f"Processing snapshot {i+1}/{len(snapshots)} from {readable_date}...")
        
        content = get_snapshot_content(timestamp, original_url)
        
        if content:
            html_filename = save_html_to_file(app_id, timestamp, content)
            app_data = extract_app_data(content)
            app_data['timestamp'] = timestamp
            app_data['snapshot_url'] = f"https://web.archive.org/web/{timestamp}/{original_url}"
            
            if html_filename:
                app_data['html_file'] = html_filename
                with open(progress_file, 'a') as f:
                    f.write(f"{timestamp}\n")
            else:
                app_data['html_file'] = "Failed to save HTML"
            
            save_to_csv(app_data, csv_filename, fields)
            print(f"Data extracted and saved for snapshot from {readable_date}")
            if html_filename:
                print(f"HTML content saved to {html_filename}")
        else:
            print(f"Skipping snapshot from {readable_date} - could not retrieve content")
        
        time.sleep(1)
    
    print(f"All data has been saved to {csv_filename} for App ID: {app_id}")

def main():
    # Read the list of App IDs from the file app_id_names.txt
    if not os.path.exists("app_id_names.txt"):
        print("app_id_names.txt file not found.")
        return

    with open("app_id_names.txt", "r") as f:
        app_ids = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(app_ids)} App IDs to process.")
    
    for app_id in app_ids:
        process_app(app_id)
        time.sleep(5)  # Optional delay between processing different apps

if __name__ == "__main__":
    main()
