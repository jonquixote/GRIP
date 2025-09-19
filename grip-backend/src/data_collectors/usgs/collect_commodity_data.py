#!/usr/bin/env python3
"""
Script to collect USGS historical data for a specific commodity from 1996-2025
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from data_collectors.usgs_collector import USGSCollector

def collect_commodity_data(commodity_name, start_year=1996, end_year=2025):
    """Collect historical data for a specific commodity from 1996-2025"""
    print(f"Collecting USGS data for {commodity_name} from {start_year} to {end_year}...")
    
    # Validate year range
    if start_year < 1996 or end_year > 2025:
        print("Warning: This script is designed to work with years 1996-2025")
    
    # Initialize collector
    collector = USGSCollector()
    
    # Collect historical data
    historical_data = collector.collect_historical_data(
        commodity=commodity_name, 
        start_year=start_year, 
        end_year=end_year
    )
    
    print(f"Collected {len(historical_data)} records")
    
    # Save to file
    filename = f"{commodity_name}_data_{start_year}_{end_year}.json"
    with open(filename, 'w') as f:
        json.dump(historical_data, f, indent=2)
    
    print(f"Data saved to {filename}")
    
    # Show sample data
    if historical_data:
        print("\nSample records:")
        for i, record in enumerate(historical_data[:3]):
            print(f"  {i+1}. {record}")
    
    # Show summary message
    total_years = end_year - start_year + 1
    if historical_data:
        # Group data by year to see which years were successfully collected
        years_with_data = set()
        for record in historical_data:
            years_with_data.add(record.get('year'))
        
        years_collected = len(years_with_data)
        print(f"\nSummary: Successfully collected data for {years_collected} out of {total_years} years.")
        
        if years_collected < total_years:
            # Find which years are missing
            all_years = set(range(start_year, end_year + 1))
            missing_years = all_years - years_with_data
            if missing_years:
                print(f"Missing data for years: {sorted(missing_years)}")
        else:
            print("All requested years were successfully collected!")
    else:
        print(f"\nSummary: No data was collected for {commodity_name} from {start_year} to {end_year}.")
        print(f"All {total_years} years failed to return data.")
    
    return historical_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python collect_commodity_data.py <commodity_name> [start_year] [end_year]")
        print("Example: python collect_commodity_data.py copper 1996 2025")
        sys.exit(1)
    
    commodity_name = sys.argv[1]
    start_year = int(sys.argv[2]) if len(sys.argv) > 2 else 1996
    end_year = int(sys.argv[3]) if len(sys.argv) > 3 else 2025
    
    collect_commodity_data(commodity_name, start_year, end_year)