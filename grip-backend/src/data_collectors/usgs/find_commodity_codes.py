#!/usr/bin/env python3
"""
Script to find correct commodity codes by testing a range of possibilities
"""
import requests
import pdfplumber
import io

def test_commodity_code_range(commodity_name, url_name, code_range, year='97'):
    """
    Test a range of commodity codes to find the correct one
    
    Args:
        commodity_name (str): Human-readable commodity name
        url_name (str): URL-friendly commodity name
        code_range (range): Range of codes to test (e.g., range(1, 100))
        year (str): 2-digit year (default '97')
        
    Returns:
        list: List of successful codes
    """
    print(f"Testing {commodity_name} ({url_name}) with codes {code_range.start}-{code_range.stop-1}")
    
    base_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs"
    successful_codes = []
    
    for code_num in code_range:
        code = f"{code_num:02d}"  # Format as 2-digit string
        url = f"{base_url}/{url_name}/{code}03{year}.pdf"
        
        try:
            # Try a HEAD request first to check if the file exists
            head_response = requests.head(url, timeout=10)
            if head_response.status_code == 200:
                print(f"  Found potential match: {code} at {url}")
                
                # Download and verify the PDF content
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    pdf_file = io.BytesIO(response.content)
                    
                    with pdfplumber.open(pdf_file) as pdf:
                        if len(pdf.pages) > 0:
                            # Extract text from the first page
                            first_page = pdf.pages[0]
                            text = first_page.extract_text()
                            
                            if text:
                                # Check if the expected commodity is mentioned in the header
                                if commodity_name.lower() in text.lower()[:500]:  # First 500 chars
                                    print(f"    ✓ CONFIRMED: PDF contains '{commodity_name}'")
                                    successful_codes.append({
                                        "code": code,
                                        "url": url
                                    })
                                else:
                                    print(f"    ✗ UNRELATED: PDF doesn't contain '{commodity_name}'")
                            else:
                                print(f"    ? NO TEXT: Could not extract text")
                        else:
                            print(f"    ? NO PAGES: PDF has no pages")
                else:
                    print(f"    ✗ DOWNLOAD FAILED: {response.status_code}")
            # else:
            #     print(f"    Code {code}: Not found (404)")
                    
        except Exception as e:
            # Only print errors for codes we expect might work
            if code_num in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]:
                print(f"    Code {code}: Error - {str(e)[:50]}")
    
    return successful_codes

def main():
    print("Commodity Code Finder")
    print("=" * 30)
    
    # Commodities we need to find codes for
    commodities_to_find = [
        {"name": "Kyanite", "url_name": "kyanite"},
        {"name": "Fluorspar", "url_name": "fluorspar"},
        {"name": "Bismuth", "url_name": "bismuth"},
        {"name": "Gallium", "url_name": "gallium"},
        {"name": "Vermiculite", "url_name": "vermiculite"},
        {"name": "Thallium", "url_name": "thallium"},
        {"name": "Indium", "url_name": "indium"},
        {"name": "Asbestos", "url_name": "asbestos"},
        {"name": "Zinc", "url_name": "zinc"},
        {"name": "Diatomite", "url_name": "diatomite"},
        {"name": "Vanadium", "url_name": "vanadium"},
        {"name": "Feldspar", "url_name": "feldspar"},
        {"name": "Germanium", "url_name": "germanium"},
        {"name": "Mercury", "url_name": "mercury"},
        {"name": "Gypsum", "url_name": "gypsum"},
        {"name": "Iodine", "url_name": "iodine"},
        {"name": "Boron", "url_name": "boron"},
        {"name": "Cadmium", "url_name": "cadmium"},
        {"name": "Antimony", "url_name": "antimony"},
        {"name": "Garnet", "url_name": "garnet"},
        {"name": "Bromine", "url_name": "bromine"},
        {"name": "Chromium", "url_name": "chromium"},
        {"name": "Tungsten", "url_name": "tungsten"},
        {"name": "Molybdenum", "url_name": "molybdenum"}
    ]
    
    # Test a focused range first (based on what we know about the numbering system)
    # From our analysis, codes seem to be in the 01-99 range, with specific allocations
    test_range = range(1, 100)
    
    results = {}
    
    for commodity in commodities_to_find:
        print(f"\n--- Finding code for {commodity['name']} ---")
        successful = test_commodity_code_range(
            commodity["name"], 
            commodity["url_name"], 
            test_range, 
            "97"
        )
        
        if successful:
            print(f"  ✓ Found {len(successful)} working codes:")
            for s in successful:
                print(f"    Code {s['code']}: {s['url']}")
            results[commodity["url_name"]] = successful
        else:
            print(f"  ? No codes found in range {test_range.start}-{test_range.stop-1}")
            results[commodity["url_name"]] = []
    
    # Summary
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    
    for url_name, codes in results.items():
        if codes:
            code_list = [c['code'] for c in codes]
            print(f"{url_name}: {', '.join(code_list)}")
        else:
            print(f"{url_name}: Not found")

if __name__ == "__main__":
    main()