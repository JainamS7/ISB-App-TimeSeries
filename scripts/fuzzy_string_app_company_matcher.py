import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import process, fuzz

def main():
    # Load Data
    df_apps = pd.read_csv('apps-newl-1_clean.csv')
    df_companies = pd.read_excel('companylist.xlsx', sheet_name=0)
    df_matched = pd.read_excel('Company-App Matching v1.xlsx', sheet_name=0)

    # Exclude Already Matched Apps
    matched_set = set(zip(
        df_matched['APP_NAME'].str.lower().fillna(''),
        df_matched['DEVELOPER'].str.lower().fillna('')
    ))
    def is_matched(row):
        return (row['APP_NAME'].lower(), row['DEVELOPER'].lower()) in matched_set
    df_apps_to_match = df_apps[~df_apps.apply(is_matched, axis=1)].copy()

    # Prepare Text Fields for NLP
    df_apps_to_match['app_text'] = (
        df_apps_to_match['APP_NAME'].fillna('') + ' ' +
        df_apps_to_match['DEVELOPER'].fillna('') + ' ' +
        df_apps_to_match.get('DESCRIPTION', '').fillna('')
    )
    df_companies['company_text'] = (
        df_companies['Company Name'].fillna('') + ' ' +
        df_companies['Category'].fillna('') + ' ' +
        df_companies['Sector'].fillna('') + ' ' +
        df_companies['Business Model'].fillna('') + ' ' +
        df_companies['Company Overview'].fillna('')
    )

    # Generate NLP Embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    app_texts = df_apps_to_match['app_text'].tolist()
    company_texts = df_companies['company_text'].tolist()
    app_embeddings = model.encode(app_texts, convert_to_tensor=True)
    company_embeddings = model.encode(company_texts, convert_to_tensor=True)

    # Compute Cosine Similarity Matrix
    similarity_matrix = util.cos_sim(app_embeddings, company_embeddings)

    # Parameters for Matching
    threshold = 0.50         # NLP threshold
    fuzzy_threshold = 90     # Fuzzy string matching threshold (0-100 scale)
    batch_size = 10
    csv_file = 'app_company_matches_fuzzy_nlp.csv'
    file_exists = os.path.isfile(csv_file)
    rows_to_write = []

    # Process Each App
    for i, idx in enumerate(df_apps_to_match.index):
        app_row = df_apps_to_match.loc[idx]
        app_name = app_row['APP_NAME'].strip().lower()
        sim_scores = similarity_matrix[i]

        # Get best NLP match
        best_idx = sim_scores.argsort(descending=True)[0].item()
        best_score = sim_scores[best_idx].item()
        nlp_match_company = df_companies.iloc[best_idx]['Company Name']

        # Use RapidFuzz to find best fuzzy match against all company names
        company_names = df_companies['Company Name'].tolist()
        fuzzy_match, fuzzy_score, _ = process.extractOne(
            app_name, [name.lower() for name in company_names], scorer=fuzz.ratio
        )
        
        # Decide which match to use:
        # If fuzzy score is high, override NLP match.
        if fuzzy_score >= fuzzy_threshold:
            final_match = fuzzy_match.title()  # assuming title case for company name
            final_similarity = None  # Not applicable for fuzzy match
        elif best_score >= threshold:
            final_match = nlp_match_company
            final_similarity = best_score
        else:
            final_match = None
            final_similarity = None

        # Optional: Rule-based override for known cases
        if app_name == 'jupiter':
            final_match = 'Jupiter'
            final_similarity = None

        rows_to_write.append({
            'APP_NAME': app_row['APP_NAME'],
            'DEVELOPER': app_row['DEVELOPER'],
            'MATCHED_COMPANY': final_match,
            'SIMILARITY': final_similarity
        })

        # Write batch every 10 apps
        if (i + 1) % batch_size == 0:
            batch_df = pd.DataFrame(rows_to_write)
            batch_df.to_csv(csv_file, mode='a', index=False, header=(not file_exists))
            file_exists = True
            rows_to_write.clear()

    if rows_to_write:
        batch_df = pd.DataFrame(rows_to_write)
        batch_df.to_csv(csv_file, mode='a', index=False, header=(not file_exists))

    print(f"Matching complete. Results appended to '{csv_file}' in batches of {batch_size}.")

if __name__ == '__main__':
    main()
