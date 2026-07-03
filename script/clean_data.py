import pandas as pd

# 1. Load the raw downloaded dataset 
# Change 'your_downloaded_file.csv' to the exact name of your downloaded file
raw_file_name = "cleaned_google_maps_business_nagpur.csv" 

try:
    df_raw = pd.read_csv(raw_file_name)
    print(f"Successfully loaded raw data! Total rows: {len(df_raw)}, Total columns: {len(df_raw.columns)}")
except FileNotFoundError:
    print(f"Error: Could not find '{raw_file_name}' in your current directory. Please check the file name.")
    exit()

# 2. Define the exact columns we need and map them to clean names
# Apify's standard names are usually 'title', 'categoryName', 'totalScore', 'reviewsCount', 'city', 'website'
column_mapping = {
    'title': 'Name',
    'categoryName': 'Category',
    'totalScore': 'Rating',
    'reviewsCount': 'Reviews',
    'city': 'Location_Area',
    'website': 'Website_URL'
}

# In case your specific scraper variation used alternative field naming structures:
fallback_mapping = {
    'name': 'Name',
    'category': 'Category',
    'rating': 'Rating',
    'userRatingCount': 'Reviews',
    'address': 'Location_Area',
    'websiteUri': 'Website_URL'
}

# Check which set of columns exists in your file and filter down
available_cols = {}
for raw_col, clean_name in column_mapping.items():
    if raw_col in df_raw.columns:
        available_cols[raw_col] = clean_name
    else:
        # Check fallback names if main names aren't present
        for fb_col, fb_clean in fallback_mapping.items():
            if fb_clean == clean_name and fb_col in df_raw.columns:
                available_cols[fb_col] = clean_name

# Filter the raw dataset down to ONLY our required columns, ignoring the rest
df_filtered = df_raw[list(available_cols.keys())].rename(columns=available_cols)

# 3. Clean and Standardize Data Types
# Fill missing metrics safely
df_filtered['Rating'] = df_filtered['Rating'].fillna(0.0).astype(float)
df_filtered['Reviews'] = df_filtered['Reviews'].fillna(0).astype(int)
df_filtered['Category'] = df_filtered['Category'].fillna('Uncategorized').str.strip().str.title()
df_filtered['Location_Area'] = df_filtered['Location_Area'].fillna('Local Region').str.strip()

# 4. Remove exact duplicate listings (e.g. if a business showed up in multiple search terms)
df_cleaned = df_filtered.drop_duplicates(subset=['Name', 'Location_Area'])

# 5. Create our core target parameter: "Has_Website"
# 1 = Has a website, 0 = Lacks a website (This isolates your digital growth leads)
df_cleaned['Has_Website'] = df_cleaned['Website_URL'].apply(
    lambda x: 0 if pd.isna(x) or str(x).strip() == "" or str(x).lower() == 'none' else 1
)

# Rearrange columns into a clean structural matrix format
final_columns = ['Name', 'Category', 'Rating', 'Reviews', 'Location_Area', 'Has_Website']
df_final = df_cleaned[final_columns]

# 6. Save the clean, filtered data to a pristine new CSV file
output_file = "cleaned_google_maps_business_nagpur.csv"
df_final.to_csv(output_file, index=False)

print("\n--- DATA CLEANING SUMMARY ---")
print(f"Filtered out {df_raw.shape[1] - df_final.shape[1]} unnecessary metadata columns.")
print(f"Remaining active business records after deduplication: {len(df_final)}")
print("\nFirst few rows of your target matrix:")
print(df_final.head())