# Local Business Digital Deficit Diagnostic Pipeline

## 🎯 Project Overview
I set out to engineer a complete, data-driven market intelligence solution to identify and capitalize on local business web infrastructure deficits across 21 major Indian commercial hubs. Starting by scraping raw, multi-city hyperlocal data, I built a robust Python pipeline that normalized drifting schemas, dropped duplicates, and transformed raw website URLs into a clean binary digital presence flag. Through this data cleaning process, I diagnosed a massive macro digital deficit—discovering that 51.5% of established brick-and-mortar operations run without independent websites. Using an algorithmic scoring model to isolate high-intent leads into targeted lists ("Established Invisibles" and "Rising Stars"), I successfully translated these insights into a high-impact presentation deck and a dark-themed, interactive Power BI dashboard to deliver an elite B2B outreach package.

## 🛠️ Key Features Included
* **Dynamic Data Ingestion & Integration:** Ingested and consolidated raw hyperlocal business data from 21 major Indian commercial hubs into a unified database matrix.
* **Resilient Schema Alignment:** Programmed a custom Python fallback routine that maps drifting raw headers (e.g., `title` vs. `name`, `websiteUri` vs. `website`) into standard target columns without execution crashes.
* **Hyperlocal Metadata Enrichment:** Engineered localized data parsing that dynamically extracted target city parameters from source file names to patch missing geographic data cells.
* **Binary Presence Engineering:** Transformed fragmented domain strings and missing URL columns into a high-performance binary feature flag (`Has_Website`) for fast, macro-level metric calculation.
* **Algorithmic Lead Prioritization:** Developed a multi-tier opportunities filter using the advanced scoring logic: 
  $$\text{Opportunity Score} = \text{Rating} \times \ln(1 + \text{Reviews})$$
  to isolate high-intent target matrices ("Established Invisibles" vs. "Rising Stars").
* **Targeted Market Isolation:** Configured custom DAX grouping fields (`Main_City`) in Power BI to accurately isolate and visualize high-friction target cities like Surat, Jaipur, and Ludhiana.
* **Executive-Grade Reporting Interface:** Cleaned and stylized interactive table fields to surface true business-level metrics rather than bulk aggregated sums, creating an elite dashboard design.

## 💻 Tech Stack Used
* **Data Pipeline & Analytics:** Python (Pandas)
* **Interactive Visualization Engine:** Power BI Desktop (DAX Analytical Engine)
* **Target Presentation Assets:** HTML5 / CSS3
* **Storage Matrix:** CSV Flat Files

## 📈 Strategic Insights & Impact
* **The Macro Gap:** 51.5% of established brick-and-mortar operations run without an independent web footprint.
* **Primary Target Hubs:** Market stagnation is heavily concentrated in high-growth regional hubs led by Surat, Jaipur, and Ludhiana.
* **Go-To-Market (GTM) Playbook:** Outlines a value-based outreach framework utilizing loss-leader entry points (single-page landing nodes) paired with reputation API integrations to capture high-velocity revenue leakages.

## 📁 Repository Structure
```text
📁 market-intelligence-deficit-analysis
│
├── 📁 data
│   ├── master_market_analysis.csv
│   ├── top_10_established_opportunities.csv
│   └── top_10_rising_stars_opportunities.csv
│
├── 📁 scripts
│   └── run_market_analysis.py
│
├── 📁 dashboard
│   └── market_analysis_dashboard.pbix
│
├── 📁 presentation
│   └── index.html
│
└── README.md