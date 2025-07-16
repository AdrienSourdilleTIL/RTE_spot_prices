import requests
import os
import csv
from collections import defaultdict
from datetime import datetime

# Base URL for national data
url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records"

# Get today's date in ISO format to include forecast
date_limit = datetime.utcnow().strftime("%Y-%m-%dT00:00:00")

params = {
    "sort": "-date_heure",
    "where": f"date_heure >= '{date_limit}'"
}

# Fetch data
response = requests.get(url, params=params)

if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code}")
    print("Details:", response.text)
    exit()

# Group records by date
records_by_date = defaultdict(list)

for record in response.json().get("results", []):
    date_str = record["date_heure"][:10]  # YYYY-MM-DD
    records_by_date[date_str].append(record)

# Write one CSV per day (no region)
for date_str, records in records_by_date.items():
    folder_path = os.path.join("data", "raw", "national")
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"generation_{date_str}.csv"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Wrote {len(records)} records to {file_path}")
