#!/usr/bin/env python3
"""
Quick test to verify we can collect data for previously missing years
"""
import sys
import os
import json

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_collector import USGSCollector

def test_comprehensive_collection():
    """Test that we can now collect data for commodities with previously missing years"""
    print("Testing Comprehensive Data Collection")
    print("=" * 40)
    
    collector = USGSCollector()
    
    # Test a few commodities that had missing 1997-2003 data
    test_cases = [
        ("barite", [1997, 1998, 1999]),
        ("kyanite", [1997, 1998, 1999]),
        ("fluorspar", [1997, 1998, 1999]),
    ]
    
    results = {}
    
    for commodity, years in test_cases:
        print(f"\nTesting {commodity} for years {years}...")
        all_data = []
        
        for year in years:
            try:
                # Try to collect data for the year
                data = collector._collect_commodity_data_for_year(commodity, year, 'production')
                all_data.extend(data)
                print(f"  {year}: Collected {len(data)} records")
            except Exception as e:
                print(f"  {year}: Error - {e}")
        
        results[commodity] = {
            'total_records': len(all_data),
            'years_tested': len(years)
        }
        
        if all_data:
            print(f"  Total for {commodity}: {len(all_data)} records")
    
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    
    for commodity, stats in results.items():
        print(f"{commodity}: {stats['total_records']} records from {stats['years_tested']} years")
    
    return results

if __name__ == "__main__":
    test_comprehensive_collection()