#!/usr/bin/env python3
"""
Comparison script for FRED collectors
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Set the API key from the environment
os.environ['FRED_API_KEY'] = '95f42f356f5131f13257eac54897e96a'

def compare_collectors():
    print("Comparing FRED collectors...")
    
    # Test original collector
    print("\n=== Testing Original Collector ===")
    try:
        from src.data_collectors.fred_collector import FREDCollector
        original_collector = FREDCollector()
        
        # Test connection
        original_conn_result = original_collector.test_connection()
        print(f"Original collector connection: {original_conn_result['success']}")
        
        # Test commodity count
        original_commodity_count = len(original_collector.commodity_series)
        print(f"Original collector commodities: {original_commodity_count}")
        
        # Test economic indicators
        original_econ_result = original_collector.get_economic_indicators()
        original_econ_count = original_econ_result['count'] if original_econ_result['success'] else 0
        print(f"Original collector economic indicators: {original_econ_count}")
        
    except Exception as e:
        print(f"Error with original collector: {e}")
        original_conn_result = {'success': False}
        original_commodity_count = 0
        original_econ_count = 0
    
    # Test enhanced collector
    print("\n=== Testing Enhanced Collector ===")
    try:
        from src.data_collectors.enhanced_fred_collector import EnhancedFREDCollector
        enhanced_collector = EnhancedFREDCollector()
        
        # Test connection
        enhanced_conn_result = enhanced_collector.test_connection()
        print(f"Enhanced collector connection: {enhanced_conn_result['success']}")
        
        # Test commodity count
        enhanced_commodity_count = len(enhanced_collector.commodity_series)
        print(f"Enhanced collector commodities: {enhanced_commodity_count}")
        
        # Test economic indicators
        enhanced_econ_result = enhanced_collector.get_economic_indicators()
        enhanced_econ_count = enhanced_econ_result['count'] if enhanced_econ_result['success'] else 0
        print(f"Enhanced collector economic indicators: {enhanced_econ_count}")
        
    except Exception as e:
        print(f"Error with enhanced collector: {e}")
        enhanced_conn_result = {'success': False}
        enhanced_commodity_count = 0
        enhanced_econ_count = 0
    
    # Print comparison
    print("\n=== Comparison Results ===")
    print(f"Commodities: {original_commodity_count} -> {enhanced_commodity_count} ({'+' if enhanced_commodity_count > original_commodity_count else ''}{enhanced_commodity_count - original_commodity_count})")
    print(f"Economic Indicators: {original_econ_count} -> {enhanced_econ_count} ({'+' if enhanced_econ_count > original_econ_count else ''}{enhanced_econ_count - original_econ_count})")
    
    # Calculate improvement percentages
    if original_commodity_count > 0:
        commodity_improvement = ((enhanced_commodity_count - original_commodity_count) / original_commodity_count) * 100
        print(f"Commodity improvement: {commodity_improvement:.1f}%")
    
    if original_econ_count > 0:
        econ_improvement = ((enhanced_econ_count - original_econ_count) / original_econ_count) * 100
        print(f"Economic indicator improvement: {econ_improvement:.1f}%")

if __name__ == "__main__":
    compare_collectors()