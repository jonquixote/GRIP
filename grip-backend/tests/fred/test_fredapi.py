#!/usr/bin/env python3
"""
Test script to explore fredapi capabilities for accessing more commodities
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set up FRED API key from environment variable
api_key = os.getenv('FRED_API_KEY')
if not api_key:
    print("ERROR: FRED_API_KEY environment variable not set")
    sys.exit(1)

try:
    import fredapi
    fred = fredapi.Fred(api_key=api_key)
    print("SUCCESS: Connected to FRED API using fredapi")
except ImportError:
    print("ERROR: fredapi not installed")
    sys.exit(1)

# Test searching for series
print("\n=== Testing Series Search ===")
try:
    # Search for gold series
    print("Searching for gold price series...")
    gold_search = fred.search('gold price')
    print(f"Found {len(gold_search)} gold series")
    if len(gold_search) > 0:
        print("Top 3 gold series:")
        for i, (index, row) in enumerate(gold_search.head(3).iterrows()):
            print(f"  {i+1}. {row['title']} (ID: {index})")
            
    # Search for silver series
    print("\nSearching for silver price series...")
    silver_search = fred.search('silver price')
    print(f"Found {len(silver_search)} silver series")
    if len(silver_search) > 0:
        print("Top 3 silver series:")
        for i, (index, row) in enumerate(silver_search.head(3).iterrows()):
            print(f"  {i+1}. {row['title']} (ID: {index})")
            
    # Search for copper series
    print("\nSearching for copper price series...")
    copper_search = fred.search('copper price')
    print(f"Found {len(copper_search)} copper series")
    if len(copper_search) > 0:
        print("Top 3 copper series:")
        for i, (index, row) in enumerate(copper_search.head(3).iterrows()):
            print(f"  {i+1}. {row['title']} (ID: {index})")
            
    # Search for oil series
    print("\nSearching for oil price series...")
    oil_search = fred.search('crude oil price')
    print(f"Found {len(oil_search)} oil series")
    if len(oil_search) > 0:
        print("Top 3 oil series:")
        for i, (index, row) in enumerate(oil_search.head(3).iterrows()):
            print(f"  {i+1}. {row['title']} (ID: {index})")
            
except Exception as e:
    print(f"Error searching series: {e}")

# Test getting specific series data
print("\n=== Testing Series Data Retrieval ===")
try:
    # Get gold series data
    gold_series_id = 'GOLDAMGBD228NLBM'  # This is what we currently use
    print(f"Getting data for gold series {gold_series_id}...")
    try:
        gold_data = fred.get_series(gold_series_id)
        print(f"Gold data retrieved: {len(gold_data)} observations")
        print(f"Latest gold price: {gold_data.iloc[-1]}")
    except Exception as e:
        print(f"Error getting gold data: {e}")
        
    # Try to get copper data
    copper_series_id = 'PCOPPUSDM'  # What we currently use
    print(f"\nGetting data for copper series {copper_series_id}...")
    try:
        copper_data = fred.get_series(copper_series_id)
        print(f"Copper data retrieved: {len(copper_data)} observations")
        print(f"Latest copper price: {copper_data.iloc[-1]}")
    except Exception as e:
        print(f"Error getting copper data: {e}")
        
    # Try to get oil data
    oil_series_id = 'DCOILWTICO'  # What we currently use
    print(f"\nGetting data for WTI oil series {oil_series_id}...")
    try:
        oil_data = fred.get_series(oil_series_id)
        print(f"Oil data retrieved: {len(oil_data)} observations")
        print(f"Latest oil price: {oil_data.iloc[-1]}")
    except Exception as e:
        print(f"Error getting oil data: {e}")
        
except Exception as e:
    print(f"Error retrieving series data: {e}")

print("\n=== Testing Alternative Series ===")
try:
    # Search for more specific commodity indexes
    print("Searching for commodity indexes...")
    index_search = fred.search('commodity index')
    print(f"Found {len(index_search)} commodity index series")
    if len(index_search) > 0:
        print("Top 5 commodity index series:")
        for i, (index, row) in enumerate(index_search.head(5).iterrows()):
            print(f"  {i+1}. {row['title']} (ID: {index})")
            
    # Search for CRB or GSCI specifically
    print("\nSearching for CRB Index...")
    crb_search = fred.search('CRB Index')
    print(f"Found {len(crb_search)} CRB index series")
    
    print("\nSearching for GSCI...")
    gsci_search = fred.search('GSCI')
    print(f"Found {len(gsci_search)} GSCI series")
    
except Exception as e:
    print(f"Error in alternative series search: {e}")

print("\n=== Test Complete ===")