#!/usr/bin/env python3
"""
Test script to verify new economic indicators in FRED collector
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.data_collectors.fred_collector import FREDCollector

c = FREDCollector()

# Test some new economic indicators
new_indicators = {
    'Capacity_Utilization': 'CAPUTLG2211S',
    'New_Private_Housing_Permits': 'PERMIT',
    '30Y_Conventional_Mortgage_Rate': 'MORTGAGE30US',
    'Total_Assets_of_Commercial_Banks': 'TOTALSL',
    'Job_Openings': 'JTSJOL'
}

print("Testing new economic indicators...")
results = {}

for name, series_id in new_indicators.items():
    print(f"Testing {name} ({series_id})...")
    result = c.get_series_info(series_id)
    results[name] = result is not None
    if result:
        print(f"  Success: {result['title']}")
    else:
        print(f"  Failed")

print("\nResults:", results)