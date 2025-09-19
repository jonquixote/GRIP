#!/usr/bin/env python3
"""
Script to extract real commodity codes and URL patterns for 1997 from USGS Mineral Commodity Summaries
"""
import requests
import re
from bs4 import BeautifulSoup
import json

# Load the commodity data
with open('usgs_mineral_commodities.json', 'r') as f:
    commodities = json.load(f)

# Function to extract commodity code from a URL
def extract_commodity_code(url_pattern):
    """
    Extract the commodity code from a URL pattern like:
    https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs/barite/080397.pdf
    Returns the code part (e.g., '08' from '080397')
    """
    # Match the 6-digit pattern at the end before .pdf
    match = re.search(r'/(\d{6})\.pdf$', url_pattern)
    if match:
        six_digit_code = match.group(1)
        # The commodity code is the first 2 digits
        return six_digit_code[:2]
    return None

# Function to test URL patterns for a commodity
def test_commodity_urls(commodity_name, url_name):
    """
    Test various URL patterns for a commodity in 1997 to find the correct commodity code
    """
    print(f"Testing URLs for {commodity_name} ({url_name})...")
    
    # Common URL patterns for 1997
    base_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs"
    patterns = [
        f"{base_url}/{url_name}/{{code}}0397.pdf",
        f"{base_url}/{url_name}/{{code}}0497.pdf",
        f"{base_url}/{url_name}/{{code}}0597.pdf",
        f"{base_url}/{url_name}/{{code}}97.pdf"
    ]
    
    # Try codes from 01 to 99
    found_codes = []
    for code in range(1, 100):
        code_str = f"{code:02d}"  # Format as 2-digit string
        for pattern in patterns:
            url = pattern.format(code=code_str)
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    print(f"  Found valid URL: {url}")
                    found_codes.append({
                        'code': code_str,
                        'url': url,
                        'pattern': pattern
                    })
                    # Break after first match to avoid duplicates
                    break
            except requests.RequestException:
                pass  # Continue to next code/pattern
    
    return found_codes

# Main function
def main():
    # Commodities with missing 1997 data (from our earlier analysis)
    commodities_with_missing_1997 = [
        'barite', 'kyanite', 'fluorspar', 'bismuth', 'gallium', 'vermiculite',
        'thallium', 'indium', 'asbestos', 'zinc', 'diatomite', 'vanadium',
        'feldspar', 'germanium', 'mercury', 'gypsum', 'iodine', 'boron',
        'cadmium', 'antimony', 'garnet', 'bromine', 'chromium', 'tungsten',
        'molybdenum'
    ]
    
    # Filter commodities to only those with missing data
    filtered_commodities = [
        c for c in commodities 
        if c['url_name'] in commodities_with_missing_1997
    ]
    
    print(f"Found {len(filtered_commodities)} commodities with missing 1997 data")
    
    # Dictionary to store results
    results = {}
    
    # Test each commodity
    for commodity in filtered_commodities:
        name = commodity['name']
        url_name = commodity['url_name']
        
        print(f"\n--- Testing {name} ---")
        found_codes = test_commodity_urls(name, url_name)
        
        if found_codes:
            results[url_name] = found_codes
            print(f"  Found {len(found_codes)} valid codes for {name}")
        else:
            print(f"  No valid codes found for {name}")
    
    # Save results to file
    with open('commodity_codes_1997.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to commodity_codes_1997.json")
    
    # Print summary
    print("\n--- SUMMARY ---")
    for url_name, codes in results.items():
        print(f"{url_name}: {', '.join([code['code'] for code in codes])}")

if __name__ == "__main__":
    main()