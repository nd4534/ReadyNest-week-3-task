import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Force UTF-8 encoding for Windows terminal safety
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Set visual aesthetics for the charts
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 1. Load the compiled dataset
try:
    df = pd.read_csv("data/cleaned/master_market_analysis.csv")
    print(f"📊 Loaded Master Matrix successfully: {len(df)} unique business records found.")
except Exception as e:
    print(f"❌ Error loading master file: {e}")
    exit()
    # --- NEW FIX: Standardize Location_Area down to the Main City ---
main_cities = [
    'Ahmedabad', 'Bengaluru', 'Chandigarh', 'Chennai', 'Delhi', 'Gurugram', 
    'Hyderabad', 'Indore', 'Jaipur', 'Kochi', 'Kolkata', 'Lucknow', 'Ludhiana', 
    'Mohali', 'Mumbai', 'Nagpur', 'Patna', 'Pune', 'Surat', 'Vadodara', 'Visakhapatnam'
]

def map_to_main_city(location_str):
    if pd.isna(location_str):
        return 'Unknown'
    loc_lower = str(location_str).lower()
    # Check if any of our major core cities are mentioned in the text string
    for city in main_cities:
        if city.lower() in loc_lower:
            return city
    return 'Other'

# Clean up the column so the chart groups them beautifully
df['Location_Area'] = df['Location_Area'].apply(map_to_main_city)
# Filter out 'Other' or 'Unknown' if you only want the clean 21 core targets
df = df[df['Location_Area'] != 'Other']

# Ensure standard types
df['Rating'] = df['Rating'].astype(float)
df['Reviews'] = df['Reviews'].astype(int)
df['Has_Website'] = df['Has_Website'].astype(int)

# --- ADVANCED SECTORAL & GEOGRAPHIC INSIGHTS GENERATOR ---

# 1. Base Metrics
total_biz = len(df)
no_web_df = df[df['Has_Website'] == 0]
total_no_web = len(no_web_df)
no_web_percentage = (total_no_web / total_biz) * 100

# 2. Category-wise Comparison Data Aggregation
cat_comparison = df.groupby('Category').agg(
    Total_Count=('Name', 'count'),
    No_Website_Count=('Has_Website', lambda x: (x == 0).sum())
).reset_index()
cat_comparison['Offline_Rate_%'] = (cat_comparison['No_Website_Count'] / cat_comparison['Total_Count']) * 100
# Filter out minor categories for better data integrity
major_cats = cat_comparison[cat_comparison['Total_Count'] >= 5].sort_values(by='Offline_Rate_%', ascending=False)

# 3. Area-wise Insights Aggregation
area_comparison = df.groupby('Location_Area').agg(
    Total_Count=('Name', 'count'),
    No_Website_Count=('Has_Website', lambda x: (x == 0).sum()),
    Average_Rating=('Rating', 'mean'),
    Gross_Reviews=('Reviews', 'sum')
).reset_index()
area_comparison['Offline_Rate_%'] = (area_comparison['No_Website_Count'] / area_comparison['Total_Count']) * 100
area_insights_sorted = area_comparison.sort_values(by='Total_Count', ascending=False)

# 4. Extract High Opportunity Zones (High volume of businesses + High Offline Rate)
# Definition: Cities with offline rates greater than the national average and meaningful data volume
high_op_zones = area_comparison[
    (area_comparison['Offline_Rate_%'] > no_web_percentage) & 
    (area_comparison['Total_Count'] >= area_comparison['Total_Count'].median())
].sort_values(by='Offline_Rate_%', ascending=False)


# Write out the structural, multi-tiered Strategic Brief
with open("market_metrics_summary.txt", "w", encoding="utf-8") as f:
    f.write("=====================================================================\n")
    f.write("     COMPLETE MARKET INTELLIGENCE MATRIX: DIGITAL PRESENCE REPORT\n")
    f.write("=====================================================================\n\n")
    
    f.write("## 1. MACRO PRESENCE DIAGNOSTICS\n")
    f.write(f" * Total Unique Business Records Compiled: {total_biz}\n")
    f.write(f" * Gross Digital Deficit (No Website)   : {total_no_web} locations\n")
    f.write(f" * National Digital Cap Gap Ratio       : {no_web_percentage:.2f}%\n")
    f.write(" * Structural Brief: Over half of the high-traffic local businesses mapped\n")
    f.write("   rely entirely on third-party platform discovery. They maintain zero independent\n")
    f.write("   digital real estate, exposing them to extreme platform algorithm risks.\n\n")
    
    f.write("## 2. CATEGORY-WISE COMPARISON (TOP DIGITALLY DRIFTING VERTICALS)\n")
    f.write(" Below are the sectors showing the largest disconnect between high physical utility\n")
    f.write(" and independent online infrastructure (Minimum sample size: 5 businesses):\n\n")
    f.write(f" {'Category':<25} | {'Total Sample':<12} | {'No Website':<10} | {'Offline Rate %':<14}\n")
    f.write("-" * 70 + "\n")
    for _, row in major_cats.head(10).iterrows():
        f.write(f" {row['Category']:<25} | {int(row['Total_Count']):<12} | {int(row['No_Website_Count']):<10} | {row['Offline_Rate_%']:.1f}%\n")
    f.write("\n * Industry Takeaway: Service-heavy and highly transactional businesses possess\n")
    f.write("   the lowest digital footprint, creating an instant target market for landing pages.\n\n")
    
    f.write("## 3. AREA-WISE INSIGHTS & INFRASTRUCTURE DATA\n")
    f.write(" Comprehensive regional layout sorting total data volume, customer evaluation baselines,\n")
    f.write(" and absolute web infrastructure adoption markers:\n\n")
    f.write(f" {'Location / City':<18} | {'Total Biz':<10} | {'Avg Rating':<10} | {'Gross Reviews':<13} | {'Offline Rate %':<14}\n")
    f.write("-" * 75 + "\n")
    for _, row in area_insights_sorted.iterrows():
        f.write(f" {row['Location_Area']:<18} | {int(row['Total_Count']):<10} | {row['Average_Rating']:<10.2f} | {int(row['Gross_Reviews']):<13} | {row['Offline_Rate_%']:.1f}%\n")
        
    f.write("\n## 4. DESIGNATED HIGH OPPORTUNITY ZONES\n")
    f.write(" These target cities feature dense, highly-reputed local business footprints but suffer from\n")
    f.write(f" offline structural gaps that exceed the national average baseline of {no_web_percentage:.1f}%:\n\n")
    for _, row in high_op_zones.iterrows():
        f.write(f" 📍 {row['Location_Area'].upper()} REGION\n")
        f.write(f"    - Market Stagnation Metric: {row['Offline_Rate_%']:.1f}% operations lack a website.\n")
        f.write(f"    - Local Competitive Trust : {int(row['Gross_Reviews'])} organic customer evaluations processed.\n")
        f.write(f"    - Strategy: Prioritize B2B outreach here. The ratio of consumer volume to web presence is highly asymmetric.\n\n")
        
    f.write("## 5. CORE GO-TO-MARKET (GTM) SOLUTIONS & FRAMEWORK\n")
    f.write(" ➡️ [Tactic A: The Loss-Leader Foot-in-the-Door Strategy]\n")
    f.write("     Do not pitch high-cost multi-page platforms initially. Offer low-friction landing\n")
    f.write("     pages with quick-action booking funnels or localized QR-code digital menus.\n\n")
    f.write(" ➡️ [Tactic B: Leverage the Network Effect via Review Aggregation]\n")
    f.write("     Use their high review volumes as structural leverage. Show them how an independent\n")
    f.write("     domain pulling in live Google API reviews increases local search authority over corporate chains.\n\n")
    f.write(" ➡️ [Tactic C: Value-Based Value Pricing]\n")
    f.write("     Frame the web solution not as an expense, but as a leak-plugging asset. Contrast the cost\n")
    f.write("     of a simple deployment against the value of lost foot traffic going to competitors with sites.\n")
    f.write("\n=====================================================================\n")

print("📝 Done! market_metrics_summary.txt now contains structural Category Comparisons, Area Insights, and High Opportunity Zones.")

# --- VISUALIZATION 1: Global Digital Presence (Pie Chart) ---
plt.figure(figsize=(6, 6))
plt.pie([total_biz - total_no_web, total_no_web], 
        labels=['Has Website', 'No Website'], 
        autopct='%1.1f%%', 
        colors=['#2ecc71', '#e74c3c'], 
        startangle=140, 
        explode=(0, 0.05))
plt.title("Overall Digital Presence across Target Markets")
plt.savefig("01_overall_digital_presence.png", dpi=300, bbox_inches='tight')
plt.close()

# --- ANALYSIS 2: HIGH OPPORTUNITY ZONES (By City/Location) ---
# Group by location and calculate the percentage of businesses without websites
city_metrics = df.groupby('Location_Area').agg(
    Total_Businesses=('Name', 'count'),
    No_Website_Count=('Has_Website', lambda x: (x == 0).sum())
).reset_index()
city_metrics['No_Website_Share_%'] = (city_metrics['No_Website_Count'] / city_metrics['Total_Businesses']) * 100
city_metrics = city_metrics.sort_values(by='No_Website_Share_%', ascending=False)

# --- VISUALIZATION 2: Area-wise Insight (Bar Chart) ---
plt.figure(figsize=(14, 6))
sns.barplot(data=city_metrics, x='Location_Area', y='No_Website_Share_%', palette='Reds_r')
plt.xticks(rotation=45, ha='right')
plt.title("High Opportunity Zones: Share of Businesses Lacking Websites by City")
plt.ylabel("% of Businesses with No Website")
plt.xlabel("City / Location")
plt.tight_layout()
plt.savefig("02_city_opportunity_zones.png", dpi=300)
plt.close()

# --- ANALYSIS 3: CATEGORY-WISE COMPARISON ---
cat_metrics = df.groupby('Category').agg(
    Total_Businesses=('Name', 'count'),
    No_Website_Count=('Has_Website', lambda x: (x == 0).sum())
).reset_index()
# Filter out sparse categories with fewer than 5 records for better statistical signal
cat_metrics = cat_metrics[cat_metrics['Total_Businesses'] >= 5]
cat_metrics['No_Website_Share_%'] = (cat_metrics['No_Website_Count'] / cat_metrics['Total_Businesses']) * 100
cat_metrics = cat_metrics.sort_values(by='No_Website_Share_%', ascending=False)

# --- VISUALIZATION 3: Category-wise Comparison (Bar Chart) ---
plt.figure(figsize=(14, 6))
sns.barplot(data=cat_metrics.head(15), x='No_Website_Share_%', y='Category', palette='mako')
plt.title("Top Business Categories Lacking a Digital Presence (Min. 5 businesses)")
plt.xlabel("% of Businesses with No Website")
plt.ylabel("Business Segment")
plt.tight_layout()
plt.savefig("03_category_digital_gap.png", dpi=300)
plt.close()

# --- ANALYSIS 4: OPPORTUNITY FINDING (DUAL STRATEGIC LISTS) ---

# Core baseline conditions (No website, established presence)
no_web_df = df[df['Has_Website'] == 0].copy()

# Ensure numpy approximation fallback for score math stability
def calculate_opp_score(rating, reviews):
    import numpy as np
    return rating * np.log1p(reviews)

# =====================================================================
# LIST A: THE ESTABLISHED INVISIBLES (High Reviews + High Ratings)
# =====================================================================
leads_a = no_web_df[(no_web_df['Rating'] >= 4.0) & (no_web_df['Reviews'] >= 5000)].copy()
leads_a['Opportunity_Score'] = leads_a.apply(lambda r: calculate_opp_score(r['Rating'], r['Reviews']), axis=1)

top_10_established = leads_a.sort_values(by=['Opportunity_Score', 'Reviews'], ascending=False).head(10)
top_10_established_clean = top_10_established[['Name', 'Category', 'Rating', 'Reviews', 'Location_Area']]
top_10_established_clean.to_csv("top_10_established_opportunities.csv", index=False)

# =====================================================================
# LIST B: THE HIGH-VELOCITY RISING STARS (Ultra-High Ratings + Growth Stage)
# =====================================================================
leads_b = no_web_df[(no_web_df['Rating'] >= 4.5) & (no_web_df['Reviews'] >= 10) & (no_web_df['Reviews'] < 50)].copy()
leads_b['Opportunity_Score'] = leads_b.apply(lambda r: calculate_opp_score(r['Rating'], r['Reviews']), axis=1)

top_10_rising = leads_b.sort_values(by=['Opportunity_Score', 'Reviews'], ascending=False).head(10)
top_10_rising_clean = top_10_rising[['Name', 'Category', 'Rating', 'Reviews', 'Location_Area']]
top_10_rising_clean.to_csv("top_10_rising_stars_opportunities.csv", index=False)

# --- Print Outputs out directly to the Terminal ---
print("\n🎯 LIST A: TOP 10 ESTABLISHED MARKET LEADERS (Lacking Websites)")
print("-" * 80)
print(top_10_established_clean.to_string(index=False))

print("\n🚀 LIST B: TOP 10 HIGH-VELOCITY RISING STARS (Lacking Websites)")
print("-" * 80)
print(top_10_rising_clean.to_string(index=False))

print("\n🎉 Success! Both discrete strategic targeting sheets have been exported to your directory.")
