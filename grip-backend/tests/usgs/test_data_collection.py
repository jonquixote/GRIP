#!/usr/bin/env python3
"""
Test script to verify we can now collect data for previously missing commodities
"""
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_collector import USGSCollector

def test_data_collection():
    """Test that we can now collect data for previously missing commodities"""
    print("Testing Data Collection for Previously Missing Commodities")
    print("=" * 60)
    
    collector = USGSCollector()
    
    # Test a few commodities that had missing 1997 data
    test_commodities = [
        "barite",
        "kyanite", 
        "fluorspar",
        "bismuth",
        "gallium"
    ]
    
    for commodity in test_commodities:
        print(f"\nTesting {commodity} for 1997...")
        try:
            # Try to collect data for 1997
            data = collector._collect_commodity_data_for_year(commodity, 1997, 'production')
            if data:
                print(f"  ✓ Successfully collected {len(data)} records for {commodity}")
                # Show first record as example
                if len(data) > 0:
                    print(f"    Example: {data[0]['country']} - {data[0]['production_volume']} metric tons")
            else:
                print(f"  ? No data collected for {commodity} (may be expected)")
        except Exception as e:
            print(f"  ✗ Error collecting data for {commodity}: {e}")

if __name__ == "__main__":
    test_data_collection()