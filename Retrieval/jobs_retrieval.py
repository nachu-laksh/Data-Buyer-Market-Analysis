from datetime import datetime
import json

import requests

job_timestamp = int(datetime.now().timestamp())

# Your SerpApi API key
API_KEY = "977ff908379a03a4d9c72dc5b71abe7d5cf7ce139c01d8221d0afbb1381e5d49"

# Define API parameters
params = {
    "api_key": API_KEY,
    "engine": "google_jobs",
    "hl": "en", # Language (English)
    "gl": "us", # Location (USA)
    "location": "United States",
    "q": "data scientist",
    "no_cache": True,
}

all_results = []
calls = 0

while True:
    # Make the API request
    response = requests.get("https://serpapi.com/search", params=params)
    calls += 1

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        job_results = data.get("jobs_results", [])
        if job_results:
            all_results.extend(job_results)
        else:
            break
        
        pagination_info = data.get("serpapi_pagination")
        next_page_token = pagination_info.get("next_page_token") if pagination_info else None
        if next_page_token:
            params["next_page_token"] = next_page_token
        else:
            break
    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

    if calls == 400:
        break

with open(f"data_scientist_{job_timestamp}.json", "w", encoding="utf-8") as file:
    json.dump(all_results, file, ensure_ascii=False, indent=4)
