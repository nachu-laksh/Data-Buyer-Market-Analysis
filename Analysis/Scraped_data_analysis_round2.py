# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 17:12:48 2025

@author: Nachu
"""

import pandas as pd

# Load dataset
df = pd.read_csv(r"C:\Users\Nachu\OneDrive - University of Pittsburgh\Others\Final folders\cleaned_json_googlejobs_round2_marketing.csv")  


# Define keywords related to potential data buyers
marketing_keywords = [
    "data acquisition", "external data", "third-party data", "alternative data",
    "data procurement", "data sourcing", "data partnerships","fraud data",
    "market data","third party data","market research",
    "data marketplace","alternative data sources"
    #expanded list that probably indicates external data requirement, but not directly related to data buying
    "marketing analytics",
    "customer data",
    "audience insights",
    "marketing intelligence",
    "market intelligence"
    "advertising analytics",
    "consumer insights",
    "customer segmentation",
    "brand analytics",
    "cross-channel marketing",
    "media planning",
    "customer behavior analysis",
    "data-driven marketing",
    "retail analytics",
    "advertising optimization",
    "predictive marketing",
    "market research data",
    "digital advertising data",
    "marketing insights",
    "marketing data strategy",
    "performance marketing",
    "B2B marketing data",
    "consumer demographics",
    "new market"
    "ad spend analytics"
]

# Convert keywords into a regex pattern
keyword_pattern_marketing = "|".join(marketing_keywords)

# Filter jobs where the description or responsibilities mention these keywords
filtered_jobs_marketing = df[
    df["description"].str.contains(keyword_pattern_marketing, case=False, na=False) |
    df["responsibilities"].str.contains(keyword_pattern_marketing, case=False, na=False)
]

# Save filtered results
filtered_jobs_marketing.to_csv("fil_marketing.csv", index=False)
import re
# ---- Helper Functions ----
def count_keyword_hits(text, keywords):
    if pd.isna(text):
        return 0
    return sum(1 for kw in keywords if re.search(rf"\b{kw}\b", text, flags=re.IGNORECASE))


# Compute total keyword hits across description + responsibilities
df["description_hits"] = df["description"].fillna("").apply(lambda x: count_keyword_hits(x, marketing_keywords))
df["responsibilities_hits"] = df["responsibilities"].fillna("").apply(lambda x: count_keyword_hits(x, marketing_keywords))
df["total_keyword_hits"] = df["description_hits"] + df["responsibilities_hits"]

# Filter out jobs with zero keyword hits
df_filtered = df[df["total_keyword_hits"] > 0]
df_filtered.to_csv("potential_data_buyers_allhits.csv", index=False)

# Company-level keyword summary
company_rollup = df_filtered.groupby("company_name").agg({
    "total_keyword_hits": "sum",
    "title": lambda x: ", ".join(set(x))
}).rename(columns={
    "total_keyword_hits": "total_hits",
    "title": "roles"
}).sort_values(by="total_hits", ascending=False).reset_index()

company_rollup.to_csv("marketing.csv", index=False)


# Percentage of titles without "data"
no_data_in_title = df_filtered[~df_filtered["title"].str.contains(r"\bdata\b", case=False, na=False)]
count_no_data = len(no_data_in_title)
percent_no_data = (count_no_data / len(df_filtered)) * 100

print(f"Count of job titles without the word 'data': {count_no_data:.2f}")
print(f"Percentage of such titles: {percent_no_data:.2f}%")

# Print total keyword hit count
print(df.total_keyword_hits.sum())