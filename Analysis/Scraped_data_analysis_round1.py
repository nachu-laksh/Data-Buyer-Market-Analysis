# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 09:43:59 2025

@author: Nachu
"""

import pandas as pd
import re

#Round1 retrieved data analysis

# Load the dataset
file_path = r"C:\Users\Nachu\Downloads\total_job_data_complete.csv" # Update with your file path

df = pd.read_csv(file_path)



# Define keywords related to potential data buyers
general_keywords = [
    "data acquisition", "external data", "third-party data", "alternative data",
    "data procurement", "data sourcing", "data partnerships",
    "market data","third party data","market research", "data provider","source data",
    "data marketplace","alternative data sources","data vendor", "data purchasing","buying data"
]

# Convert keywords into a regex pattern
keyword_pattern_general = "|".join(general_keywords)

# Filter jobs where the description or responsibilities mention these keywords
filtered_jobs = df[
    df["description"].str.contains(keyword_pattern_general, case=False, na=False) |
    df["responsibilities"].str.contains(keyword_pattern_general, case=False, na=False)|
    df["job_highlights"].str.contains(keyword_pattern_general, case=False, na=False)
]

# Helper function to count keyword matches in a text
def count_keyword_hits(text):
    if pd.isna(text):
        return 0
    return len(re.findall(keyword_pattern_general, text, flags=re.IGNORECASE))

# Apply function to relevant columns and sum across them
df["keyword_hits_general"] = (
    df["description"].apply(count_keyword_hits) +
    df["responsibilities"].apply(count_keyword_hits) +
    df["job_highlights"].apply(count_keyword_hits)
)

# Filter rows with at least one keyword hit
filtered_jobs = df[df["keyword_hits_general"] > 0]
print(df.keyword_hits_general.sum())