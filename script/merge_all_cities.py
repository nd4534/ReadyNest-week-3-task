import pandas as pd
import glob
import sys

# Force UTF-8 encoding for standard output to handle any weird string characters safely
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Grab all CSV files in the current directory
csv_files = glob.glob("*.csv")

# Filter out the final combined file names so we don't accidentally read an old merge
output_name = "master_market_analysis.csv"
csv_files = [f for f in csv_files if f != output_name and f != "cleaned_google_maps_business_data.csv"]

if not csv_files:
    print("Error: No city CSV files found in this folder!")
    exit()

print(f"Found {len(csv_files)} cleaned city files to combine...")

all_dataframes = []

# 2. Read each file directly since columns are already clean
for file in csv_files:
    try:
        df = pd.read_csv(file)
        
        # Strip out any empty rows just in case
        df = df.dropna(subset=['Name'])
        
        all_dataframes.append(df)
        print(f"[OK] Loaded {file} ({len(df)} rows)")
    except Exception as e:
        print(f"[ERROR] Failed to read {file}: {str(e)}")

# 3. Merge and deduplicate everything
if all_dataframes:
    df_master = pd.concat(all_dataframes, ignore_index=True)
    
    # Drop exact duplicates if the same business appears multiple times
    total_before = len(df_master)
    df_master = df_master.drop_duplicates(subset=['Name', 'Location_Area'])
    total_after = len(df_master)
    
    # Save the absolute master copy
    df_master.to_csv(output_name, index=False)
    
    print("\n--- CONSOLIDATION SUMMARY ---")
    print(f"Successfully stacked all datasets!")
    print(f"Total rows collected: {total_before}")
    print(f"Total unique records after deduplication: {total_after}")
    print(f"Master dataset securely saved as: '{output_name}'")
else:
    print("Processing failed: No data could be compiled.")