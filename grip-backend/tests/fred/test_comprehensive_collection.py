#!/usr/bin/env python3
"""
Test script for enhanced FRED collector with comprehensive data collection
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set the API key from the environment
os.environ['FRED_API_KEY'] = '95f42f356f5131f13257eac54897e96a'

def test_comprehensive_data_collection():
    print("Testing enhanced FRED collector with comprehensive data collection...")
    
    try:
        from src.data_collectors.enhanced_fred_collector import EnhancedFREDCollector
        collector = EnhancedFREDCollector()
        
        print("Testing connection...")
        conn_result = collector.test_connection()
        print("Connection test result:", conn_result)
        
        if conn_result['success']:
            print("\nTesting comprehensive data collection for oil prices...")
            # Test with oil prices which typically have rich data
            result = collector.collect_price_data('oil_wti')
            print("Oil WTI collection result:", result['success'])
            if result['success']:
                print(f"  Current data points: {result['counts']['current_data']}")
                print(f"  First release points: {result['counts']['first_release_data']}")
                print(f"  Revision history points: {result['counts']['all_releases_data']}")
                print(f"  Vintage dates: {result['counts']['vintage_dates']}")
                print(f"  Series info available: {result['series_info'] is not None}")
            else:
                print("  Error:", result.get('error', 'Unknown error'))
                
            print("\nTesting comprehensive data collection for copper...")
            result = collector.collect_price_data('copper')
            print("Copper collection result:", result['success'])
            if result['success']:
                print(f"  Current data points: {result['counts']['current_data']}")
                print(f"  First release points: {result['counts']['first_release_data']}")
                print(f"  Revision history points: {result['counts']['all_releases_data']}")
                print(f"  Vintage dates: {result['counts']['vintage_dates']}")
                print(f"  Series info available: {result['series_info'] is not None}")
            else:
                print("  Error:", result.get('error', 'Unknown error'))
        else:
            print("Connection failed, cannot proceed with tests")
            
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_data_collection()