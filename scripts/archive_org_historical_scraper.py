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

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
target_url = "https://play.google.com/store/apps/details?id=com.indiainfoline"

# User agent
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

def get_wayback_snapshots(url):
    """Get all available snapshots from Wayback Machine for a URL"""
    encoded_url = quote(url, safe='')
    cdx_api_url = f"https://web.archive.org/cdx/search/cdx?url={encoded_url}&output=json&fl=timestamp,original,statuscode,digest,length&filter=statuscode:200&collapse=timestamp:6"
    
    try:
        response = requests.get(cdx_api_url, headers=headers, verify=False)
        if response.status_code == 200:
            snapshots = response.json()
            # Remove the header row
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
    """Get the content of a specific snapshot with retry logic"""
    wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
    
    for attempt in range(max_retries):
        try:
            # Add randomization to delay to appear more human-like
            delay = base_delay + random.uniform(1, 5)
            print(f"Waiting {delay:.2f} seconds before request...")
            time.sleep(delay)
            
            response = requests.get(wayback_url, headers=headers, verify=False, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get snapshot content: {response.status_code}")
                # Increase delay for next attempt
                base_delay *= 2
        except ConnectionError as e:
            print(f"Connection error on attempt {attempt+1}/{max_retries}: {e}")
            # Exponential backoff with jitter
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
            # Try alternative selectors for different Wayback Machine versions
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

def save_html_to_file(timestamp, html_content):
    """Save the complete HTML content to a text file"""
    # Create directory if it doesn't exist
    html_dir = "html_snapshots"
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    
    # Format timestamp for filename
    formatted_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y%m%d_%H%M%S')
    
    # Create filename
    filename = os.path.join(html_dir, f"tatacapital_app_{formatted_date}.html")
    
    # Save HTML content to file
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        return True
    except Exception as e:
        print(f"Error saving HTML to file: {e}")
        return False

def save_to_csv(app_data, csv_filename, fields):
    """Save a single entry to CSV file"""
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Write the data row
        writer.writerow(app_data)

def main():
    print(f"Fetching snapshots for {target_url}...")
    snapshots = get_wayback_snapshots(target_url)
    print(f"Found {len(snapshots)} snapshots")
    
    # Create CSV file
    csv_filename = "grow_app_data_timeseries_final_3.csv"
    
    # Update the fields list in the main function
    fields = [
        'timestamp', 'snapshot_url', 'app_name', 'developer', 'rating', 
        'reviews', 'downloads', 'description', 'last_updated', 
        'version', 'size', 'content_rating', 'whats_new', 'full_description',
        'html_file'  # New field to store the HTML file reference
    ]
    progress_file = "scraping_progress.txt"
    processed_timestamps = set()
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            processed_timestamps = set(line.strip() for line in f)
    # Process each snapshot
    for i, snapshot in enumerate(snapshots):
        timestamp = snapshot[0]
        original_url = snapshot[1]
        if timestamp in processed_timestamps:
            print(f"Skipping already processed snapshot {i+1}/{len(snapshots)} from {timestamp}")
            continue
        # Convert timestamp to readable date for display
        readable_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        print(f"Processing snapshot {i+1}/{len(snapshots)} from {readable_date}...")
        
        # Get snapshot content
        content = get_snapshot_content(timestamp, original_url)
        
        if content:
            # Save the complete HTML to a file
            html_saved = save_html_to_file(timestamp, content)
            formatted_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y%m%d_%H%M%S')
            html_filename = f"html_snapshots/tatacapital_app_{formatted_date}.html"
            
            # Extract app data
            app_data = extract_app_data(content)
            
            # Add timestamp and snapshot URL
            app_data['timestamp'] = timestamp
            app_data['snapshot_url'] = f"https://web.archive.org/web/{timestamp}/{original_url}"
            
            # Add HTML file reference
            if html_saved:
                app_data['html_file'] = html_filename
                with open(progress_file, 'a') as f:
                  f.write(f"{timestamp}\n")
            else:
                app_data['html_file'] = "Failed to save HTML"
            
            # Save to CSV
            save_to_csv(app_data, csv_filename, fields)
            
            print(f"Data extracted and saved for snapshot from {readable_date}")
            if html_saved:
                print(f"HTML content saved to {html_filename}")
        else:
            print(f"Skipping snapshot from {readable_date} - could not retrieve content")
        
        # Be nice to the Wayback Machine servers
        time.sleep(1)
    
    print(f"All data has been saved to {csv_filename}")

if __name__ == "__main__":
    main()
