"""
NLP-Based App-Company Matching Algorithm
========================================

This script implements semantic matching between fintech applications and companies
using state-of-the-art natural language processing techniques. It's a critical
component of the ISB Fintech Research Project that enables accurate app-company
relationship identification.

Methodology:
- Utilizes Sentence Transformers for semantic text embeddings
- Implements cosine similarity for relationship scoring
- Processes app descriptions and company profiles for matching
- Applies configurable similarity thresholds for quality control
- Excludes previously matched pairs to avoid duplication

Technical Approach:
1. Text Preprocessing: Combines multiple fields (name, description, category)
2. Embedding Generation: Creates vector representations using pre-trained models
3. Similarity Computation: Calculates cosine similarity matrix
4. Threshold Filtering: Applies minimum similarity requirements
5. Batch Processing: Outputs results in configurable batch sizes

Key Features:
- Uses 'all-MiniLM-L6-v2' sentence transformer model
- Configurable similarity threshold (default: 0.50)
- Memory-efficient batch processing (default: 10 records)
- Excludes already matched app-company pairs
- Outputs structured CSV with similarity scores

Performance Optimizations:
- Tensor-based computations for speed
- Batch writing to reduce I/O operations
- Memory management for large datasets
- Incremental processing support

Input Data:
- apps-newl-1_clean.csv: Cleaned fintech application dataset
- companylist.xlsx: Traxcn fintech company database
- Company-App Matching v1.xlsx: Previously matched pairs

Output:
- app_company_matches_crude_all.csv: New matches with similarity scores

Usage:
    python nlpmatch.py

Dependencies:
    - sentence-transformers: Semantic text embeddings
    - pandas: Data manipulation and analysis
    - torch: Tensor computations (via sentence-transformers)

Author: ISB Fintech Research Team
Project: Advanced App-Company Relationship Mining
Institution: Indian School of Business (ISB)
"""

import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

def main():
    # -------------------------------------------------------------------------
    # 1. Load Data
    # -------------------------------------------------------------------------
    df_apps = pd.read_csv('apps-newl-1_clean.csv')          # Adjust delimiter if needed
    df_companies = pd.read_excel('companylist.xlsx', sheet_name=0)
    df_matched = pd.read_excel('Company-App Matching v1.xlsx', sheet_name=0)

    # -------------------------------------------------------------------------
    # 2. Exclude Already Matched Apps
    # -------------------------------------------------------------------------
    matched_set = set(zip(
        df_matched['APP_NAME'].str.lower().fillna(''),
        df_matched['DEVELOPER'].str.lower().fillna('')
    ))

    # Filter out apps that have already been matched
    def is_matched(row):
        return (row['APP_NAME'].lower(), row['DEVELOPER'].lower()) in matched_set

    df_apps_to_match = df_apps[~df_apps.apply(is_matched, axis=1)].copy()

    # -------------------------------------------------------------------------
    # 3. Prepare Text Fields for NLP
    # -------------------------------------------------------------------------
    # Combine relevant fields from apps
    df_apps_to_match['app_text'] = (
        df_apps_to_match['APP_NAME'].fillna('') + ' ' +
        df_apps_to_match['DEVELOPER'].fillna('') + ' ' +
        df_apps_to_match.get('DESCRIPTION', '').fillna('')
    )

    # Combine relevant fields from companies
    df_companies['company_text'] = (
        df_companies['Company Name'].fillna('') + ' ' +
        df_companies['Category'].fillna('') + ' ' +
        df_companies['Sector'].fillna('') + ' ' +
        df_companies['Business Model'].fillna('') + ' ' +
        df_companies['Company Overview'].fillna('')
    )

    # -------------------------------------------------------------------------
    # 4. Generate Embeddings
    # -------------------------------------------------------------------------
    model = SentenceTransformer('all-MiniLM-L6-v2')

    app_texts = df_apps_to_match['app_text'].tolist()
    company_texts = df_companies['company_text'].tolist()

    app_embeddings = model.encode(app_texts, convert_to_tensor=True)
    company_embeddings = model.encode(company_texts, convert_to_tensor=True)

    # -------------------------------------------------------------------------
    # 5. Compute Similarity Scores
    # -------------------------------------------------------------------------
    similarity_matrix = util.cos_sim(app_embeddings, company_embeddings)

    # -------------------------------------------------------------------------
    # 6. Find Matches and Append to CSV in Batches of 10
    # -------------------------------------------------------------------------
    # Threshold for a "valid" match
    threshold = 0.50
    batch_size = 10

    # If the CSV doesn't exist, we'll need headers. Otherwise, we append without headers.
    csv_file = 'app_company_matches_crude_all.csv'
    file_exists = os.path.isfile(csv_file)

    # Prepare to collect rows in memory and write them in batches of 10
    rows_to_write = []
    df_index = df_apps_to_match.index  # We'll iterate over the matched DataFrame's indices

    for i, idx in enumerate(df_index):
        app_row = df_apps_to_match.loc[idx]
        sim_scores = similarity_matrix[i]

        # Sort companies by descending similarity and get the best match
        best_idx = sim_scores.argsort(descending=True)[0].item()
        best_score = sim_scores[best_idx].item()
        best_company = df_companies.iloc[best_idx]['Company Name']

        # If best score is below threshold, set MATCHED_COMPANY to None
        matched_company = best_company if best_score >= threshold else None

        # Add row to our batch
        rows_to_write.append({
            'APP_NAME': app_row['APP_NAME'],
            'DEVELOPER': app_row['DEVELOPER'],
            'MATCHED_COMPANY': matched_company,
            'SIMILARITY': best_score if matched_company else None
        })

        # After every 10 apps, write to CSV
        if (i + 1) % batch_size == 0:
            batch_df = pd.DataFrame(rows_to_write)
            batch_df.to_csv(csv_file, mode='a', index=False, header=(not file_exists))
            file_exists = True
            rows_to_write.clear()

    # Write any remaining rows (if total apps % 10 != 0)
    if rows_to_write:
        batch_df = pd.DataFrame(rows_to_write)
        batch_df.to_csv(csv_file, mode='a', index=False, header=(not file_exists))

    print(f"Matching complete. Results appended to '{csv_file}' in batches of {batch_size}.")

if __name__ == '__main__':
    main()
