# import requests
# from bs4 import BeautifulSoup
# import csv
# import time

# # Input data structure - make sure to include all your entries
# data = [{
#     "href": "https://www.apkmirror.com/apk/google-inc/tez-a-new-payments-app-by-google/google-pay-save-and-pay-263-1-2-release/",
#     "innerText": "Google Pay: Save and Pay 263.1.2",
#     "dateyear_utc": "January 27, 2025 GMT+0530"
#   },
#   # ... (paste all your other entries here)
# ]

# # headers = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
# #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
# #     "Accept-Language": "en-US,en;q=0.5",
# #     "Connection": "keep-alive",
# # }
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Referer": "https://www.apkmirror.com/",
#     "DNT": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "TE": "trailers"
# }

# def scrape_notes():
#     output = []

#     for entry in data:
#         if not entry.get('dateyear_utc'):
#             continue

#         url = entry['href']
#         print(f"Processing: {url}")

#         try:
#             response = requests.get(url, headers=headers)
#             time.sleep(3)

#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 notes_divs = soup.find_all('div', class_=['notes', 'wrapText'])

#                 notes_content = []
#                 for div in notes_divs:
#                     paragraphs = div.find_all('p')
#                     notes_content.extend([p.get_text(strip=True) for p in paragraphs])

#                 output.append({
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': '\n'.join(notes_content) if notes_content else 'No notes found'
#                 })
#             else:
#                 print(f"Error {response.status_code} for {url}")
#                 output.append({
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': f"Error: HTTP Status {response.status_code}"
#                 })

#         except Exception as e:
#             print(f"Error processing {url}: {str(e)}")
#             output.append({
#                 'href': url,
#                 'innerText': entry['innerText'],
#                 'dateyear_utc': entry['dateyear_utc'],
#                 'notes': f"Error: {str(e)}"
#             })

#     return output

# def save_to_csv(results):
#     filename = 'apk_notes.csv'
#     with open(filename, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['href', 'innerText', 'dateyear_utc', 'notes'])
#         writer.writeheader()
#         writer.writerows(results)
#     print(f"\nData saved to {filename} in current directory")

# if __name__ == '__main__':
#     results = scrape_notes()
#     save_to_csv(results)
#     print("Scraping completed. You can find the CSV file in your project folder.")



# import requests
# from bs4 import BeautifulSoup
# import csv
# import time
# import random
# import os
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Input data structure - make sure to include all your entries
# data = [
#     {
#     "href": "https://www.apkmirror.com/apk/dreamplug-technologies-private-limited/cred-most-rewarding-credit-card-bill-payment-app/cred-upi-credit-cards-bills-5-0-3-7-release/",
#     "innerText": "CRED: UPI, Credit Cards, Bills 5.0.3.7",
#     "dateyear_utc": "March 18, 2025 GMT+0530"
#   },
#    {
#     "href": "https://www.apkmirror.com/apk/google-inc/tez-a-new-payments-app-by-google/google-pay-save-and-pay-272-1-2-release/",
#     "innerText": "Google Pay: Save and Pay 272.1.2",
#     "dateyear_utc": "March 26, 2025 GMT+0530"
#     },
#   # ... (paste all your other entries here)
# ]

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Referer": "https://www.apkmirror.com/",
#     "DNT": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "TE": "trailers"
# }

# # Configure retry strategy
# retry_strategy = Retry(
#     total=5,
#     status_forcelist=[429, 500, 502, 503, 504],
#     allowed_methods=["GET"],
#     backoff_factor=2,
#     respect_retry_after_header=True
# )

# # Create session with retry
# session = requests.Session()
# session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

# # def get_existing_entries():
# #     existing_urls = set()
# #     filename = 'apk_notes.csv'
    
# #     for row in links:
# #         href_value = row.get('href')
# #         if href_value:
# #             existing_urls.add(href_value)
# #     return existing_urls

# def save_to_csv(entry):
#     """Save a single entry to CSV, writing header if needed"""
#     filename = 'cred_trial.csv'
#     file_exists = os.path.exists(filename)
    
#     with open(filename, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['href', 'innerText', 'dateyear_utc', 'notes'])
        
#         if not file_exists:
#             writer.writeheader()
        
#         writer.writerow(entry)
# import re
# def scrape_notes():
#     # existing_urls = get_existing_entries()
#     new_entries = [entry for entry in data]
    
#     # Shuffle entries to randomize request pattern
#     # random.shuffle(new_entries)
    
#     for index, entry in enumerate(new_entries):
#         if not entry.get('dateyear_utc'):
#             continue

#         url = entry['href']
#         print(f"Processing ({index+1}/{len(new_entries)}): {url}")

#         try:
#             # Random delay with normal distribution (avg 8-12s)
#             delay = random.uniform(0, 1) + abs(random.gauss(0, 1))
#             time.sleep(delay)

#             response = session.get(url, headers=headers)
            
#             # Handle 429 specifically
#             if response.status_code == 429:
#                 retry_after = int(response.headers.get('Retry-After', 20))
#                 print(f"Rate limited. Waiting {retry_after} seconds...")
#                 time.sleep(retry_after)
#                 response = session.get(url, headers=headers)  # Retry once

#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 notes_divs = soup.find_all('div', class_=re.compile(r'^notes wrapText'))
#                 # notes_divs = soup.find_all('div', class_='notes wrapText')

#                 notes_content = []
#                 for div in notes_divs:
#                     # Remove version links if present
#                     for strong in div.find_all('strong'):
#                         if 'From version' in strong.text:
#                             strong.decompose()
                    
#                     paragraphs = div.find_all('p')
#                     notes_content.extend([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

#                 # Create and save successful entry
#                 result_entry = {
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': '\n'.join(notes_content) if notes_content else 'No notes found'
#                 }
#                 save_to_csv(result_entry)
#                 print(f"Saved entry: {url}")

#             else:
#                 # Create and save error entry
#                 error_entry = {
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': f"Error: HTTP Status {response.status_code}"
#                 }
#                 save_to_csv(error_entry)
#                 print(f"Error {response.status_code} for {url}")

#         except Exception as e:
#             # Create and save exception entry
#             error_entry = {
#                 'href': url,
#                 'innerText': entry['innerText'],
#                 'dateyear_utc': entry['dateyear_utc'],
#                 'notes': f"Error: {str(e)}"
#             }
#             save_to_csv(error_entry)
#             print(f"Error processing {url}: {str(e)}")
#             # Wait longer after exceptions
#             time.sleep(30)

# if __name__ == '__main__':
#     scrape_notes()
#     print("Scraping completed. Check apk_notes.csv for results.")



# import requests
# from bs4 import BeautifulSoup
# import csv
# import time
# import random
# import os
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Input data structure - include all your entries here
# data = [
    # {
    #     "href": "https://www.apkmirror.com/apk/dreamplug-technologies-private-limited/cred-most-rewarding-credit-card-bill-payment-app/cred-upi-credit-cards-bills-5-0-3-7-release/",
    #     "innerText": "CRED: UPI, Credit Cards, Bills 5.0.3.7",
    #     "dateyear_utc": "March 18, 2025 GMT+0530"
    # },
    # {
    # "href": "https://www.apkmirror.com/apk/google-inc/tez-a-new-payments-app-by-google/google-pay-save-and-pay-272-1-2-release/",
    # "innerText": "Google Pay: Save and Pay 272.1.2",
    # "dateyear_utc": "March 26, 2025 GMT+0530"
    # },
#     # ... (other entries)
# ]

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Referer": "https://www.apkmirror.com/",
#     "DNT": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "TE": "trailers"
# }

# # Configure retry strategy
# retry_strategy = Retry(
#     total=5,
#     status_forcelist=[429, 500, 502, 503, 504],
#     allowed_methods=["GET"],
#     backoff_factor=2,
#     respect_retry_after_header=True
# )

# # Create session with retry
# session = requests.Session()
# session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

# def save_to_csv(entry):
#     """Save a single entry to CSV, writing header if needed."""
#     filename = 'cred_trial.csv'
#     file_exists = os.path.exists(filename)
    
#     with open(filename, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['href', 'innerText', 'dateyear_utc', 'notes'])
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(entry)

# def scrape_notes():
#     new_entries = [entry for entry in data if entry.get('dateyear_utc')]
    
#     for index, entry in enumerate(new_entries):
#         url = entry['href']
#         print(f"Processing ({index+1}/{len(new_entries)}): {url}")
        
#         try:
#             # Random delay (approximately 8-12s on average)
#             delay = random.uniform(0, 1) + abs(random.gauss(0, 1))
#             time.sleep(delay)
            
#             response = session.get(url, headers=headers)
            
#             # Handle HTTP 429 (rate limited)
#             if response.status_code == 429:
#                 retry_after = int(response.headers.get('Retry-After', 20))
#                 print(f"Rate limited. Waiting {retry_after} seconds...")
#                 time.sleep(retry_after)
#                 response = session.get(url, headers=headers)  # Retry once
            
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 # Use CSS selector to get the div elements with both classes 'notes' and 'wrapText'
#                 notes_divs = soup.select("div.notes.wrapText")
                
#                 notes_content = []
#                 # Process each div to extract text
#                 for div in notes_divs:
#                     # Remove <strong> tags that mention "From version"
#                     for strong in div.find_all('strong'):
#                         if 'From version' in strong.get_text():
#                             strong.decompose()
                    
#                     # Extract text from <p> tags, if available
#                     paragraphs = div.find_all('p')
#                     if paragraphs:
#                         for p in paragraphs:
#                             text = p.get_text(strip=True)
#                             if text:
#                                 notes_content.append(text)
#                     else:
#                         # Fallback: grab all text in the div if no <p> tags exist
#                         text = div.get_text(strip=True)
#                         if text:
#                             notes_content.append(text)
                
#                 final_notes = "\n".join(notes_content) if notes_content else "No notes found"
                
#                 result_entry = {
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': final_notes
#                 }
#                 save_to_csv(result_entry)
#                 print(f"Saved entry: {url}")
#             else:
#                 # Save error entry for non-200 responses
#                 error_entry = {
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': f"Error: HTTP Status {response.status_code}"
#                 }
#                 save_to_csv(error_entry)
#                 print(f"Error {response.status_code} for {url}")
                
#         except Exception as e:
#             # Save exception entry and wait longer after exceptions
#             error_entry = {
#                 'href': url,
#                 'innerText': entry['innerText'],
#                 'dateyear_utc': entry['dateyear_utc'],
#                 'notes': f"Error: {str(e)}"
#             }
#             save_to_csv(error_entry)
#             print(f"Error processing {url}: {str(e)}")
#             time.sleep(30)

# if __name__ == '__main__':
#     scrape_notes()
#     print("Scraping completed. Check cred_trial.csv for results.")


# import requests
# from bs4 import BeautifulSoup
# import csv
# import time

# # Input data structure
# data = [
#   {
#     "href": "https://www.apkmirror.com/apk/tri-o-tech-solutions-pvt-ltd/fampay-prepaid-card-payments-for-teenagers/famapp-by-trio-upi-card-3-10-9-release/",
#     "innerText": "FamApp by Trio: UPI & Card 3.10.9",
#     "dateyear_utc": "March 22, 2025 GMT+0530"
#   }
# ]

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "Cache-Control": "max-age=0",
# }

# def scrape_notes():
#     output = []

#     for entry in data:
#         if not entry.get('dateyear_utc'):
#             continue

#         url = entry['href']
#         print(f"Processing: {url}")

#         try:
#             response = requests.get(url, headers=headers)
#             time.sleep(3)  # Respectful delay between requests

#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 notes_divs = soup.find_all('div', class_=['notes', 'wrapText'])

#                 notes_content = []
#                 for div in notes_divs:
#                     paragraphs = div.find_all('p')
#                     notes_content.extend([p.get_text(strip=True) for p in paragraphs])

#                 output.append({
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': '\n'.join(notes_content)
#                 })
#             else:
#                 output.append({
#                     'href': url,
#                     'innerText': entry['innerText'],
#                     'dateyear_utc': entry['dateyear_utc'],
#                     'notes': f"Error: HTTP Status {response.status_code}"
#                 })

#         except Exception as e:
#             output.append({
#                 'href': url,
#                 'innerText': entry['innerText'],
#                 'dateyear_utc': entry['dateyear_utc'],
#                 'notes': f"Error: {str(e)}"
#             })

#     return output

# def save_to_csv(results):
#     filename = 'fampay_notes.csv'
#     with open(filename, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['href', 'innerText', 'dateyear_utc', 'notes'])
#         writer.writeheader()
#         writer.writerows(results)
#     print(f"Data saved to {filename}")

# if __name__ == '__main__':
#     results = scrape_notes()
#     save_to_csv(results)
#     print("Scraping completed.")



import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import csv
import time

# Input data structure
data = [
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-6-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.6.4",
    "dateyear_utc": "March 24, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-6-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.6.3",
    "dateyear_utc": "March 14, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-6-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.6.2",
    "dateyear_utc": "March 12, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-6-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.6.1",
    "dateyear_utc": "March 5, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-6-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.6.0",
    "dateyear_utc": "February 27, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-8-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.8",
    "dateyear_utc": "February 19, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-6-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.6",
    "dateyear_utc": "February 10, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.4",
    "dateyear_utc": "February 4, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.3",
    "dateyear_utc": "January 23, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.2",
    "dateyear_utc": "January 22, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.1",
    "dateyear_utc": "January 6, 2024 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-5-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.5.0",
    "dateyear_utc": "December 26, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-7-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.7",
    "dateyear_utc": "December 11, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-6-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.6",
    "dateyear_utc": "November 28, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-5-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.5",
    "dateyear_utc": "November 14, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.4",
    "dateyear_utc": "November 10, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.3",
    "dateyear_utc": "November 5, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.2",
    "dateyear_utc": "October 29, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.1",
    "dateyear_utc": "October 23, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-4-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.4.0",
    "dateyear_utc": "October 13, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-3-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.3.1",
    "dateyear_utc": "October 1, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-3-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.3.0",
    "dateyear_utc": "September 16, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-6-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.6",
    "dateyear_utc": "September 3, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-5-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.5",
    "dateyear_utc": "August 21, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.3",
    "dateyear_utc": "August 5, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.2",
    "dateyear_utc": "July 21, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.1",
    "dateyear_utc": "July 9, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-2-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.2.0",
    "dateyear_utc": "June 27, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-1-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.1.4",
    "dateyear_utc": "June 19, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-1-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.1.3",
    "dateyear_utc": "June 8, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-1-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.1.2",
    "dateyear_utc": "June 2, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-1-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.1.1",
    "dateyear_utc": "May 26, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-1-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.1.0",
    "dateyear_utc": "May 25, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-21-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.21",
    "dateyear_utc": "May 16, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-20-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.20",
    "dateyear_utc": "May 12, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-19-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.19",
    "dateyear_utc": "April 30, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-18-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.18",
    "dateyear_utc": "April 14, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-16-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.16",
    "dateyear_utc": "April 5, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-15-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.15",
    "dateyear_utc": "April 2, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-14-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.14",
    "dateyear_utc": "March 20, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-13-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.13",
    "dateyear_utc": "March 10, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-12-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.12",
    "dateyear_utc": "March 1, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-11-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.11",
    "dateyear_utc": "February 27, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-10-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.10",
    "dateyear_utc": "February 10, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-9-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.9",
    "dateyear_utc": "January 31, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-8-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.8",
    "dateyear_utc": "January 30, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-7-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.7",
    "dateyear_utc": "January 23, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-6-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.6",
    "dateyear_utc": "January 13, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-5-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.5",
    "dateyear_utc": "January 6, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.4",
    "dateyear_utc": "January 3, 2023 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.3",
    "dateyear_utc": "December 24, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.2",
    "dateyear_utc": "December 18, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-2-0-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 2.0.1",
    "dateyear_utc": "December 9, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-7-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.7.3",
    "dateyear_utc": "December 7, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-7-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.7.1",
    "dateyear_utc": "December 2, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-18-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.18",
    "dateyear_utc": "November 16, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-17-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.17",
    "dateyear_utc": "November 14, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-15-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.15",
    "dateyear_utc": "November 6, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-13-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.13",
    "dateyear_utc": "November 4, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-14-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.14",
    "dateyear_utc": "October 29, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-11-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.11",
    "dateyear_utc": "October 9, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-10-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.10",
    "dateyear_utc": "September 29, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-9-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.9",
    "dateyear_utc": "September 24, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-8-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.8",
    "dateyear_utc": "September 21, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-7-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.7",
    "dateyear_utc": "September 9, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-6-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.6",
    "dateyear_utc": "September 2, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-5-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.5",
    "dateyear_utc": "August 30, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-4-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.4",
    "dateyear_utc": "August 19, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-3-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.3",
    "dateyear_utc": "August 13, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-2-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.2",
    "dateyear_utc": "August 9, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-1-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.1",
    "dateyear_utc": "August 7, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-6-0-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.6.0",
    "dateyear_utc": "July 30, 2022 GMT+0530"
  },
  {
    "href": "https://www.apkmirror.com/apk/jupiter-savings-bank-account-zero-balance/jupiter-digital-bank-account/jupiter-digital-bank-account-1-5-47-release/",
    "innerText": "Jupiter: UPI & Credit Cards 1.5.47",
    "dateyear_utc": "July 28, 2022 GMT+0530"
  }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    backoff_factor=1.5,
    respect_retry_after_header=True
)

# Create session with retry
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

def scrape_notes():
    output = []

    for entry in data:
        if not entry.get('dateyear_utc'):
            continue

        url = entry['href']
        print(f"Processing: {url}")

        try:
            response = session.get(url, headers=headers)
            time.sleep(2.5)  # Respectful delay between requests

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                notes_divs = soup.find_all('div', class_=['notes', 'wrapText'])

                notes_content = []
                for div in notes_divs:
                    paragraphs = div.find_all('p')
                    notes_content.extend([p.get_text(strip=True) for p in paragraphs])

                output.append({
                    'href': url,
                    'innerText': entry['innerText'],
                    'dateyear_utc': entry['dateyear_utc'],
                    'notes': '\n'.join(notes_content)
                })
            else:
                output.append({
                    'href': url,
                    'innerText': entry['innerText'],
                    'dateyear_utc': entry['dateyear_utc'],
                    'notes': f"Error: HTTP Status {response.status_code}"
                })

        except Exception as e:
            output.append({
                'href': url,
                'innerText': entry['innerText'],
                'dateyear_utc': entry['dateyear_utc'],
                'notes': f"Error: {str(e)}"
            })

    return output

def save_to_csv(results):
    filename = 'jupiter_notes.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['href', 'innerText', 'dateyear_utc', 'notes'])
        writer.writeheader()
        writer.writerows(results)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    results = scrape_notes()
    save_to_csv(results)
    print("Scraping completed.")
