#!/usr/bin/env python3
"""
Script to run the FRED collector and collect all data
"""

import sys
import os
# Add the project root to sys.path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.data_collectors.fred_collector import FREDCollector
import logging

def main():
    """Main function to run the FRED collector"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create collector instance
    collector = FREDCollector()
    
    # Test connection first
    print("Testing FRED API connection...")
    connection_result = collector.test_connection()
    print(f"Connection test result: {connection_result}")
    
    if not connection_result['success']:
        print("Failed to connect to FRED API. Please check your API key.")
        return 1
    
    # Collect all FRED data
    print("\nStarting comprehensive FRED data collection...")
    result = collector.collect_all_fred_data()
    
    if result['success']:
        print("FRED data collection completed successfully!")
        print(f"Commodities collected: {result['commodities']['total_records']} records")
        print(f"Economic indicators collected: {result['economic_indicators']['count']} indicators")
        print(f"Series metadata collected: {len(result['series_metadata'])} series")
        print(f"Search results collected: {len(result['search_results'])} searches")
        return 0
    else:
        print("FRED data collection failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())