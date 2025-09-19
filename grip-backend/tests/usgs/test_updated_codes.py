#!/usr/bin/env python3
"""
Test script to verify our updated commodity codes work correctly
"""
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collectors.usgs_commodity_codes import get_commodity_code, construct_commodity_url

def test_commodity_codes():
    """Test that our updated commodity codes work correctly"""
    print("Testing Updated Commodity Codes")
    print("=" * 40)
    
    # Test cases with the codes we've verified
    test_cases = [
        ("barite", 1997, "08"),
        ("kyanite", 1997, "37"),
        ("fluorspar", 1997, "28"),
        ("bismuth", 1997, "11"),
        ("gallium", 1997, "46"),
        ("vermiculite", 1997, "71"),
        ("thallium", 1997, "84"),
        ("indium", 1997, "49"),
        ("asbestos", 1997, "07"),
        ("zinc", 1997, "72"),
        ("diatomite", 1997, "25"),
        ("vanadium", 1997, "70"),
        ("feldspar", 1997, "26"),
        ("germanium", 1997, "22"),
        ("mercury", 1997, "43"),
        ("gypsum", 1997, "32"),
        ("iodine", 1997, "77"),
        ("boron", 1997, "12"),
        ("antimony", 1997, "06"),
        ("garnet", 1997, "41"),
        ("bromine", 1997, "13"),
        ("chromium", 1997, "18"),
        ("tungsten", 1997, "68"),
        ("molybdenum", 1997, "47"),
    ]
    
    all_passed = True
    
    for commodity, year, expected_code in test_cases:
        actual_code = get_commodity_code(commodity, year)
        if actual_code == expected_code:
            print(f"✓ {commodity}: {actual_code} (expected {expected_code})")
        else:
            print(f"✗ {commodity}: {actual_code} (expected {expected_code})")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")
    
    return all_passed

def test_url_construction():
    """Test that URL construction works with our updated codes"""
    print("\nTesting URL Construction")
    print("=" * 40)
    
    # Test a few commodities
    test_commodities = [
        ("barite", 1997),
        ("kyanite", 1997),
        ("fluorspar", 1997),
    ]
    
    for commodity, year in test_commodities:
        url = construct_commodity_url(commodity, year)
        if url:
            print(f"{commodity} ({year}): {url}")
        else:
            print(f"{commodity} ({year}): Failed to construct URL")

if __name__ == "__main__":
    # Test commodity codes
    test_commodity_codes()
    
    # Test URL construction
    test_url_construction()