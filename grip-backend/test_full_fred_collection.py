#!/usr/bin/env python3
"""
Test script to run comprehensive FRED data collection
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set the API key from the environment
os.environ['FRED_API_KEY'] = '95f42f356f5131f13257eac54897e96a'

def test_comprehensive_fred_collection():
    print("Testing comprehensive FRED data collection...")
    
    try:
        from src.data_collectors.enhanced_fred_collector import EnhancedFREDCollector
        collector = EnhancedFREDCollector()
        
        print("Testing connection...")
        conn_result = collector.test_connection()
        print("Connection test result:", conn_result['success'])
        
        if conn_result['success']:
            print("\nStarting comprehensive FRED data collection...")
            result = collector.collect_all_fred_data()
            
            if result['success']:
                print("Comprehensive FRED data collection completed successfully!")
                print(f"Commodities collected: {result['commodities']['success']}")
                print(f"Economic indicators collected: {result['economic_indicators']['success']}")
                print(f"Series metadata collected: {len(result['series_metadata'])} series")
                print(f"Revision data collected for: {len(result['revisions_data'])} series")
                print(f"Search results collected: {len(result['search_results'])} terms")
                print(f"Category results collected: {len(result['category_results'])} categories")
                print(f"Release results collected: {len(result['release_results'])} releases")
            else:
                print("Comprehensive data collection failed")
                print("Error:", result.get('error', 'Unknown error'))
        else:
            print("Connection failed, cannot proceed with comprehensive collection")
            
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_fred_collection()