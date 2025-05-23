"""
Wayback Machine Historical Data Scraper
=======================================

This script integrates with the Internet Archive's Wayback Machine to collect
historical Google Play Store snapshots for fintech applications. It implements
intelligent snapshot discovery and retrieval strategies for comprehensive
temporal data collection.

Core Functionality:
- CDX API integration for efficient snapshot discovery
- Multi-selector HTML parsing for different page layouts
- Robust data extraction across various Google Play Store versions
- CSV output with temporal organization
- Error handling and retry mechanisms

Technical Features:
- Wayback Machine CDX API for snapshot enumeration
- BeautifulSoup parsing with multiple selector fallbacks
- Timestamp-based data organization
- SSL verification disabled for archive.org compatibility
- Comprehensive app metadata extraction

Data Extraction Points:
- App name and developer information
- User ratings and review counts
- Download statistics and version information
- App descriptions and update notes
- Content ratings and size information
- Last updated dates and version numbers

Extraction Strategy:
1. Discover available snapshots using CDX API
2. Filter snapshots by HTTP status code (200 only)
3. Retrieve HTML content with error handling
4. Parse content using multiple selector strategies
5. Extract structured data with fallback mechanisms
6. Save both individual records and batch CSV output

Performance Considerations:
- Efficient snapshot discovery via CDX API
- Respectful request timing with delays
- Memory-efficient streaming processing
- Incremental CSV writing for large datasets

Usage:
    # Configure target URL in script
    target_url = "https://play.google.com/store/apps/details?id=com.example.app"
    python wayback_scraper.py

Dependencies:
    - requests: HTTP client for API and content retrieval
    - pandas: Data structure management
    - beautifulsoup4: HTML parsing and data extraction
    - urllib3: SSL configuration management

Output Format:
    CSV file with temporal app data including ratings, downloads,
    descriptions, and metadata across historical snapshots

Author: ISB Fintech Research Team
Project: Historical Fintech App Data Collection
Institution: Indian School of Business (ISB)
"""

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
from urllib.parse import quote

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
target_url = "https://play.google.com/store/apps/details?id=com.balancehero.truebalance"

# User agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
headers = {"User-Agent": user_agent}

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

def get_snapshot_content(timestamp, url):
    """Get the content of a specific snapshot"""
    wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
    try:
        response = requests.get(wayback_url, headers=headers, verify=False, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to get snapshot content: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting snapshot content: {e}")
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
    
    return app_data

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
    csv_filename = "truebalance_app_data_timeseries_main.csv"
    
    # Define all possible fields we might extract
    fields = [
        'timestamp', 'snapshot_url', 'app_name', 'developer', 'rating', 
        'reviews', 'downloads', 'description', 'last_updated', 
        'version', 'size', 'content_rating'
    ]
    
    # Process each snapshot
    for i, snapshot in enumerate(snapshots):
        timestamp = snapshot[0]
        original_url = snapshot[1]
        
        # Convert timestamp to readable date for display
        readable_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        print(f"Processing snapshot {i+1}/{len(snapshots)} from {readable_date}...")
        
        # Get snapshot content
        content = get_snapshot_content(timestamp, original_url)
        
        if content:
            # Extract app data
            app_data = extract_app_data(content)
            
            # Add timestamp and snapshot URL
            app_data['timestamp'] = timestamp
            app_data['snapshot_url'] = f"https://web.archive.org/web/{timestamp}/{original_url}"
            
            # Save this entry to CSV immediately
            save_to_csv(app_data, csv_filename, fields)
            
            print(f"Data extracted and saved for snapshot from {readable_date}")
        else:
            print(f"Skipping snapshot from {readable_date} - could not retrieve content")
        
        # Be nice to the Wayback Machine servers
        time.sleep(1)
    
    print(f"All data has been saved to {csv_filename}")

if __name__ == "__main__":
    main()
