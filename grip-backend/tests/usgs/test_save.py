#!/usr/bin/env python3
import sys
import os
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_collector import USGSCollector

def test_save():
    print("Testing data collection and save...")
    
    # Create collector
    collector = USGSCollector()
    
    # Collect data for one commodity for a few years
    print("Collecting data for gold (2020-2021)...")
    data = collector.collect_historical_data(
        commodity="gold",
        start_year=2020,
        end_year=2021
    )
    
    print(f"Collected {len(data)} records")
    
    # Create the correct data directory path
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'usgs')
    print(f"Data directory: {data_dir}")
    
    # Ensure directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to file with correct path
    filename = os.path.join(data_dir, "gold_test_data_2020_2021.json")
    print(f"Saving to: {filename}")
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Data saved successfully!")
    
    # Verify file exists and has content
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            saved_data = json.load(f)
        print(f"Verified: File contains {len(saved_data)} records")
    else:
        print("Error: File was not created")

if __name__ == "__main__":
    test_save()