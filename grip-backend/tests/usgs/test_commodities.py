#!/usr/bin/env python3
import sys
import os
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_collector import USGSCollector

def test_multiple_commodities():
    print("Testing data collection for multiple commodities...")
    
    # Test a few key commodities
    test_commodities = [
        {"name": "Gold", "url_name": "gold"},
        {"name": "Copper", "url_name": "copper"},
        {"name": "Silver", "url_name": "silver"},
        {"name": "Aluminum", "url_name": "aluminum"},
        {"name": "Lithium", "url_name": "lithium"}
    ]
    
    collector = USGSCollector()
    
    # Create results directory (correct path)
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'usgs')
    data_dir = os.path.abspath(data_dir)  # Ensure we have the absolute path
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"Data will be saved to: {data_dir}")
    
    results = []
    
    for i, commodity in enumerate(test_commodities):
        name = commodity["name"]
        url_name = commodity["url_name"]
        
        print(f"[{i+1}/{len(test_commodities)}] Testing {name}...")
        
        try:
            # Collect data for recent years only to speed up testing
            data = collector.collect_historical_data(
                commodity=url_name,
                start_year=2020,
                end_year=2022
            )
            
            print(f"  Collected {len(data)} records")
            
            if data:
                # Save to file (using correct path)
                filename = os.path.join(data_dir, f"{url_name}_test_data_2020_2022.json")
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"  Saved to {filename}")
                
                results.append({
                    "name": name,
                    "url_name": url_name,
                    "records": len(data),
                    "file": filename,
                    "status": "success"
                })
            else:
                print(f"  No data collected")
                results.append({
                    "name": name,
                    "url_name": url_name,
                    "records": 0,
                    "status": "no_data"
                })
                
        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                "name": name,
                "url_name": url_name,
                "records": 0,
                "status": "error",
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successful = len([r for r in results if r["status"] == "success"])
    no_data = len([r for r in results if r["status"] == "no_data"])
    errors = len([r for r in results if r["status"] == "error"])
    
    print(f"Total commodities tested: {len(test_commodities)}")
    print(f"Successful collections: {successful}")
    print(f"No data found: {no_data}")
    print(f"Errors: {errors}")
    
    if successful > 0:
        total_records = sum(r["records"] for r in results if r["status"] == "success")
        avg_records = total_records / successful
        print(f"Total records collected: {total_records:,}")
        print(f"Average records per successful commodity: {avg_records:.1f}")
    
    print("\nDetailed results:")
    for result in results:
        if result["status"] == "success":
            print(f"  ✓ {result['name']}: {result['records']} records")
        elif result["status"] == "no_data":
            print(f"  - {result['name']}: No data")
        else:
            print(f"  ✗ {result['name']}: Error - {result['error']}")
    
    return results

if __name__ == "__main__":
    test_multiple_commodities()