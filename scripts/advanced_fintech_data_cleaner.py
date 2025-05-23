import os
import pandas as pd
import json
import time
import requests
import google.generativeai as genai
# Set your Gemini API key and endpoint (update these values based on actual API details)
GEMINI_API_KEY = "AIzaSyByvG4TfWYmrJPguAsC_LyRMiMr1W6CoLY" # or assign directly
GEMINI_ENDPOINT = "https://api.generativeai.googleapis.com/v1beta2/models/YOUR_MODEL:generateText"  # 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-001')
def clean_record_gemini(record):
    prompt = (
        "You are a data cleaning assistant. Clean and normalize the following JSON record extracted from a Play Store HTML snapshot. "
        "Ensure that:\n"
        "- All extra spaces and newlines are removed\n"
        "- Ratings are converted to numeric values\n"
        "- The number of installs is normalized (remove commas, plus signs, etc.)\n"
        "- All text fields are properly trimmed\n\n"
        "Record:\n" + json.dumps(record, ensure_ascii=False)
    )
    
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "temperature": 0,
        "maxOutputTokens": 250,
    }
    
    try:
        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Assume the API returns the cleaned JSON record in a field called "result"
        cleaned_text = result.get("result", "{}")
        cleaned_record = json.loads(cleaned_text)
        return cleaned_record
    except Exception as e:
        print("Error cleaning record with Gemini:", e)
        return record

# Load the CSV file
df = pd.read_csv("output_lxml_hdfc.csv", encoding='utf-8')
cleaned_records = []

for i, row in df.iterrows():
    record = row.to_dict()
    cleaned = clean_record_gemini(record)
    cleaned_records.append(cleaned)
    time.sleep(1)

# Save cleaned data to CSV
cleaned_df = pd.DataFrame(cleaned_records)
cleaned_df.to_csv("output_lxml_cleaned_gemini.csv", index=False, encoding='utf-8')
print("Cleaned CSV (using Gemini) written to output_lxml_cleaned_gemini.csv")
