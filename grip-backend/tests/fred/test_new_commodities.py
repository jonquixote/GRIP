#!/usr/bin/env python3
"""
Test script to verify all new commodity series are working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.data_collectors.fred_collector import FREDCollector

c = FREDCollector()
commodities = ['propane', 'heating_oil', 'diesel', 'gasoline', 'palm_oil']
results = {}

for commodity in commodities:
    print(f"Testing {commodity}...")
    result = c.collect_price_data(commodity)
    results[commodity] = result['success']
    if result['success']:
        print(f"  Success: {result['count']} records")
    else:
        print(f"  Failed: {result.get('error', 'Unknown error')}")

print("\nResults:", results)