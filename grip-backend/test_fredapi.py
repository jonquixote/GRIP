#!/usr/bin/env python3
"""
Test script to verify fredapi installation
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from fredapi import Fred
    print("fredapi imported successfully")
    
    # Test with the API key from environment
    api_key = os.getenv('FRED_API_KEY')
    if api_key:
        fred = Fred(api_key=api_key)
        print("FRED API client created successfully")
        
        # Test a simple API call
        data = fred.get_series_info('GDP')
        print("API test successful:", data['title'] if data else "No data returned")
    else:
        print("FRED_API_KEY not found in environment")
        
except ImportError as e:
    print("Failed to import fredapi:", e)
except Exception as e:
    print("Error:", e)