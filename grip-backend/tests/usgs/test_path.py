#!/usr/bin/env python3
import sys
import os
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_collector import USGSCollector

def test_paths():
    print("Testing path construction...")
    
    # Test the path that will be used in the collect_comprehensive_data.py script
    data_dir = os.path.join(os.path.dirname('./src/data_collectors/usgs/collect_comprehensive_data.py'), '..', '..', '..', 'data', 'usgs')
    data_dir = os.path.abspath(data_dir)
    
    print(f"Data directory path: {data_dir}")
    print(f"Does directory exist? {os.path.exists(data_dir)}")
    
    if not os.path.exists(data_dir):
        print("Creating directory...")
        os.makedirs(data_dir, exist_ok=True)
        print(f"Created directory: {data_dir}")
    
    # Test data collection
    print("\nTesting data collection...")
    collector = USGSCollector()
    
    # Collect a small sample of data
    data = collector.collect_historical_data(commodity='gold', start_year=2020, end_year=2021)
    print(f"Collected {len(data)} records for gold")
    
    if data:
        # Save to the correct location
        filename = os.path.join(data_dir, "gold_test_2020_2021.json")
        print(f"Saving to: {filename}")
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Data saved successfully!")
        
        # Verify file exists
        if os.path.exists(filename):
            print("File verification: SUCCESS")
            # Check file size
            file_size = os.path.getsize(filename)
            print(f"File size: {file_size} bytes")
        else:
            print("File verification: FAILED")
    else:
        print("No data collected")

if __name__ == "__main__":
    test_paths()