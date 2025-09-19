
import json
import os

def find_missing_years_for_all_commodities(directory):
    missing_years_per_commodity = {}
    for filename in os.listdir(directory):
        if filename.endswith("_data_1996_2025.json"):
            commodity_name = filename.replace("_data_1996_2025.json", "")
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Could not decode JSON from {filename}")
                    data = []

            present_years = set()
            if isinstance(data, list):
                for record in data:
                    if isinstance(record, dict) and 'year' in record:
                        present_years.add(record['year'])
            
            all_years = set(range(1996, 2026))
            missing_years = sorted(list(all_years - present_years))
            
            if missing_years:
                missing_years_per_commodity[commodity_name] = missing_years
                
    return missing_years_per_commodity

if __name__ == "__main__":
    directory = "../../../data/usgs/"
    missing_years = find_missing_years_for_all_commodities(directory)
    print(missing_years)
