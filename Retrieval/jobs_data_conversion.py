import json

import pandas as pd

def _get_responsibility_from_job_result(result):
    # If responsibilities are highlighted for the results, return the items list as a
    # long text of sentences.
    if "job_highlights" not in result:
        return None
    
    for highlight in result["job_highlights"]:
        if highlight["title"].lower() == "responsibilities":
            return ". ".join(highlight["items"])
    
    return None

def main():
    roles = ["data_procurement", "data_scientist", "data_governance", "data_analyst", "data_governance_1738635534", "data_scientist_1738635798", "data_scientist_1738635909"]

    # Combine results for different roles into one list; add the query that produced the result.
    raw_results = []
    for job_role in roles:
        role_name = "_".join(job_role.split("_")[:2])
        file_name = f"{job_role}.json"

        with open(file_name, "r", encoding="utf-8") as file:
            results = json.load(file)
            for result in results:
                result["query"] = role_name
        
        raw_results.extend(results)

    # Extract just the relevant fields from each result.
    parsed_results = []
    job_ids_seen = set()
    for result in raw_results:
        if result["job_id"] in job_ids_seen:
            continue
        job_ids_seen.add(result["job_id"])
        parsed_results.append({
            "query": result["query"],
            "job_id": result["job_id"],
            "title": result["title"],
            "company_name": result["company_name"],
            "location": result["location"],
            "description": result["description"],
            "responsibilities": _get_responsibility_from_job_result(result),
        })

    # Convert to pandas dataframe.
    df = pd.DataFrame(parsed_results)
    df.info()
    print(df)
    df.to_csv("dataset.csv", index=False)


if __name__ == "__main__":
    main()
