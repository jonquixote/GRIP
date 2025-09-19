#!/usr/bin/env python3
"""
Test script for enhanced FRED collector
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Set the API key from the environment
os.environ['FRED_API_KEY'] = '95f42f356f5131f13257eac54897e96a'

try:
    from src.data_collectors.enhanced_fred_collector import EnhancedFREDCollector
    
    print("Creating enhanced FRED collector...")
    collector = EnhancedFREDCollector()
    
    print("Testing connection...")
    result = collector.test_connection()
    print("Connection test result:", result)
    
    if result['success']:
        print("Testing data collection for a few commodities...")
        # Test with a few commodities
        commodities_to_test = ['gold', 'silver', 'copper']
        
        for commodity in commodities_to_test:
            print(f"Collecting data for {commodity}...")
            result = collector.collect_price_data(commodity)
            print(f"  Result: {result['success']}, Count: {result.get('count', 0)}")
            
        print("Testing economic indicators collection...")
        result = collector.get_economic_indicators()
        print(f"Economic indicators result: {result['success']}, Count: {result.get('count', 0)}")
        
    else:
        print("Connection failed, cannot proceed with tests")
        
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()