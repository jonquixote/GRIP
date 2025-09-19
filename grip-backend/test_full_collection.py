#!/usr/bin/env python3
"""
Test script for enhanced FRED collector with full data collection
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Set the API key from the environment
os.environ['FRED_API_KEY'] = '95f42f356f5131f13257eac54897e96a'

def test_full_data_collection():
    print("Testing enhanced FRED collector with full data collection...")
    
    try:
        from src.data_collectors.enhanced_fred_collector import EnhancedFREDCollector
        collector = EnhancedFREDCollector()
        
        # Test connection
        print("1. Testing connection...")
        conn_result = collector.test_connection()
        print(f"   Connection result: {conn_result['success']}")
        if not conn_result['success']:
            print(f"   Error: {conn_result.get('error', 'Unknown error')}")
            return
        
        # Test commodity data collection
        print("2. Testing commodity data collection...")
        commodities_result = collector.collect_all_commodities_data()
        print(f"   Commodities collected: {commodities_result['success']}")
        if commodities_result['success']:
            print(f"   Total records: {commodities_result['total_records']}")
        else:
            print(f"   Error: {commodities_result.get('error', 'Unknown error')}")
        
        # Test economic indicators
        print("3. Testing economic indicators collection...")
        indicators_result = collector.get_economic_indicators()
        print(f"   Economic indicators collected: {indicators_result['success']}")
        if indicators_result['success']:
            print(f"   Total indicators: {indicators_result['count']}")
        else:
            print(f"   Error: {indicators_result.get('error', 'Unknown error')}")
        
        # Test series info
        print("4. Testing series info retrieval...")
        series_info = collector.get_series_info('GDP')
        print(f"   Series info retrieved: {series_info is not None}")
        
        # Test search functionality
        print("5. Testing search functionality...")
        search_result = collector.search_series('gold', limit=10)
        print(f"   Search completed: {search_result['success']}")
        if search_result['success']:
            print(f"   Search results: {search_result['count']}")
        else:
            print(f"   Error: {search_result.get('error', 'Unknown error')}")
        
        # Test revisions data
        print("6. Testing revisions data collection...")
        # Use a known working series
        series_id = 'PCOPPUSDM'  # Copper price series
        all_releases = collector.get_all_releases(series_id)
        print(f"   All releases collected: {all_releases['success']}")
        if all_releases['success']:
            print(f"   Release count: {all_releases['count']}")
        
        first_release = collector.get_first_release(series_id)
        print(f"   First release collected: {first_release['success']}")
        if first_release['success']:
            print(f"   First release count: {first_release['count']}")
        
        vintage_dates = collector.get_vintage_dates(series_id)
        print(f"   Vintage dates collected: {vintage_dates['success']}")
        if vintage_dates['success']:
            print(f"   Vintage dates count: {vintage_dates['count']}")
        
        # Test comprehensive data collection
        print("7. Testing comprehensive data collection...")
        full_result = collector.collect_all_fred_data()
        print(f"   Full data collection: {full_result['success']}")
        
        print("\n=== Test Summary ===")
        print(f"Connection: {'PASS' if conn_result['success'] else 'FAIL'}")
        print(f"Commodities: {'PASS' if commodities_result['success'] else 'FAIL'}")
        print(f"Economic Indicators: {'PASS' if indicators_result['success'] else 'FAIL'}")
        print(f"Series Info: {'PASS' if series_info is not None else 'FAIL'}")
        print(f"Search: {'PASS' if search_result['success'] else 'FAIL'}")
        print(f"Revisions: {'PASS' if all([all_releases['success'], first_release['success'], vintage_dates['success']]) else 'FAIL'}")
        print(f"Full Collection: {'PASS' if full_result['success'] else 'FAIL'}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_data_collection()