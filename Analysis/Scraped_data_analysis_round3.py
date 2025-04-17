# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 17:12:48 2025

@author: Nachu
"""

import pandas as pd

import pandas as pd
import re

# Load dataset
df = pd.read_csv(r"C:\Users\Nachu\OneDrive - University of Pittsburgh\Others\Final folders\dataset_financial.csv")

# Define keywords related to potential data buyers
keywords = [
    "data acquisition", "external data", "third-party data", "alternative data",
    "data procurement", "data sourcing", "data partnerships",
    "market data", "third party data", "market research","data vendor"
    "data marketplace", "alternative data sources", 
    "data buying", "data vendor", "market intelligence data", "data provider", "source data",
    "data subscriptions", "commercial data"
]

# Convert keywords into a regex pattern
keyword_pattern = "|".join([re.escape(kw) for kw in keywords])

# Combine description and responsibilities into a single text column
df["match_text"] = df["description"].fillna("") + " " + df["responsibilities"].fillna("")

# Function to count how many keywords appear in the text
def count_keyword_hits(text):
    if pd.isna(text):
        return 0
    return len(re.findall(keyword_pattern, text, flags=re.IGNORECASE))

# Add a column with the number of keyword matches
df["keyword_hits"] = df["match_text"].apply(count_keyword_hits)

# Filter jobs with at least one keyword hit
filtered_jobs = df[df["keyword_hits"] > 0]
print(df.keyword_hits.sum())







