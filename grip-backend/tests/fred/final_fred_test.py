#!/usr/bin/env python3
"""
Final verification test for the enhanced FRED collector
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.data_collectors.fred_collector import FREDCollector
import json

def test_fred_collector():
    """Final test to verify the enhanced FRED collector functionality"""
    print("=== FRED Collector Final Verification Test ===")
    
    # Create collector instance
    collector = FREDCollector()
    
    # Test connection
    print("1. Testing FRED API connection...")
    connection_result = collector.test_connection()
    assert connection_result['success'], "FRED API connection failed"
    print("   ✓ Connection successful")
    
    # Test single commodity collection
    print("2. Testing single commodity collection (copper)...")
    copper_result = collector.collect_price_data('copper')
    assert copper_result['success'], "Copper data collection failed"
    assert copper_result['count'] > 0, "No copper data collected"
    print(f"   ✓ Collected {copper_result['count']} copper records")
    
    # Verify data file exists
    copper_data_file = os.path.join(collector.commodities_dir, 'copper', 'copper_data.json')
    assert os.path.exists(copper_data_file), "Copper data file not found"
    print("   ✓ Copper data file exists")
    
    # Verify metadata file exists
    copper_metadata_file = os.path.join(collector.metadata_dir, 'copper_metadata.json')
    assert os.path.exists(copper_metadata_file), "Copper metadata file not found"
    print("   ✓ Copper metadata file exists")
    
    # Check data file content
    with open(copper_data_file, 'r') as f:
        copper_data = json.load(f)
    assert copper_data['success'], "Copper data file indicates failure"
    assert len(copper_data['data']) > 0, "Copper data file contains no data"
    print("   ✓ Copper data file content verified")
    
    # Test all commodities collection
    print("3. Testing all commodities collection...")
    all_result = collector.collect_all_commodities_data()
    assert all_result['success'], "All commodities collection failed"
    assert all_result['total_records'] > 0, "No records collected in all commodities"
    print(f"   ✓ Collected {all_result['total_records']} total records")
    
    # Verify all commodities data file exists
    all_data_file = os.path.join(collector.data_dir, 'all_commodities_data.json')
    assert os.path.exists(all_data_file), "All commodities data file not found"
    print("   ✓ All commodities data file exists")
    
    # Test economic indicators collection
    print("4. Testing economic indicators collection...")
    indicators_result = collector.get_economic_indicators()
    assert indicators_result['success'], "Economic indicators collection failed"
    assert indicators_result['count'] > 0, "No economic indicators collected"
    print(f"   ✓ Collected {indicators_result['count']} economic indicators")
    
    # Verify economic indicators file exists
    indicators_file = os.path.join(collector.economic_indicators_dir, 'economic_indicators.json')
    assert os.path.exists(indicators_file), "Economic indicators file not found"
    print("   ✓ Economic indicators file exists")
    
    # Test search functionality
    print("5. Testing search functionality...")
    search_result = collector.search_commodity_series('gold')
    assert search_result['success'], "Search functionality failed"
    print(f"   ✓ Found {search_result['filtered_count']} gold-related series")
    
    # Verify search results file exists
    search_file = os.path.join(collector.search_results_dir, 'search_results_gold.json')
    assert os.path.exists(search_file), "Search results file not found"
    print("   ✓ Search results file exists")
    
    print("\n=== All Tests Passed! ===")
    print("The FRED collector is working correctly with organized data storage.")
    return True

if __name__ == "__main__":
    try:
        test_fred_collector()
        print("\n🎉 FRED collector verification completed successfully!")
    except Exception as e:
        print(f"\n❌ FRED collector verification failed: {e}")
        sys.exit(1)