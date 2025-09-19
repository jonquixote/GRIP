#!/usr/bin/env python3
"""
Script to verify commodity codes by checking PDF content
"""
import requests
import pdfplumber
import io
import re

def verify_commodity_from_pdf(url, expected_commodity):
    """
    Verify that a PDF at a given URL actually contains data for the expected commodity
    by checking the title on the first page.
    
    Args:
        url (str): URL to the PDF
        expected_commodity (str): Name of the expected commodity
        
    Returns:
        dict: Verification result with success flag and extracted title
    """
    try:
        # Download PDF
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return {"success": False, "error": f"Failed to download PDF: {response.status_code}"}

        pdf_file = io.BytesIO(response.content)
        
        with pdfplumber.open(pdf_file) as pdf:
            if len(pdf.pages) > 0:
                # Extract text from the first page
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                
                if text:
                    # Look for the commodity name in the first few lines
                    lines = text.split('\n')[:10]  # First 10 lines
                    page_header = ' '.join(lines)
                    
                    # Check if the expected commodity is mentioned in the header
                    if expected_commodity.lower() in page_header.lower():
                        return {
                            "success": True, 
                            "title": page_header[:100],  # First 100 characters
                            "match": True
                        }
                    else:
                        # Return what we found instead
                        return {
                            "success": True, 
                            "title": page_header[:100],  # First 100 characters
                            "match": False,
                            "found": page_header[:50]  # First 50 characters for brevity
                        }
                else:
                    return {"success": False, "error": "Could not extract text from PDF"}
            else:
                return {"success": False, "error": "PDF has no pages"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_commodity_code(commodity_name, url_name, code, year='97'):
    """
    Test a specific commodity code for a given year
    
    Args:
        commodity_name (str): Human-readable commodity name
        url_name (str): URL-friendly commodity name
        code (str): 2-digit commodity code to test
        year (str): 2-digit year (default '97')
        
    Returns:
        dict: Test result
    """
    # Construct URL
    base_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/mineral-pubs"
    url = f"{base_url}/{url_name}/{code}03{year}.pdf"
    
    print(f"Testing {commodity_name} with code {code} for year 19{year}")
    print(f"URL: {url}")
    
    # Verify the PDF content
    result = verify_commodity_from_pdf(url, commodity_name)
    
    if result["success"]:
        if result.get("match"):
            print(f"  ✓ MATCH: PDF contains '{commodity_name}'")
            return {"success": True, "code": code, "url": url}
        else:
            print(f"  ✗ NO MATCH: PDF title is '{result.get('found', 'Unknown')}'")
            return {"success": False, "code": code, "url": url, "title": result.get("title")}
    else:
        print(f"  ✗ ERROR: {result.get('error')}")
        return {"success": False, "code": code, "url": url, "error": result.get("error")}

# Test function for multiple codes
def test_multiple_codes(commodity_name, url_name, codes_to_test, year='97'):
    """
    Test multiple codes for a commodity
    """
    print(f"\n=== Testing {commodity_name} ({url_name}) ===")
    
    results = []
    for code in codes_to_test:
        result = test_commodity_code(commodity_name, url_name, code, year)
        results.append(result)
        
    # Find successful matches
    successful = [r for r in results if r["success"]]
    if successful:
        print(f"\n✓ Found {len(successful)} working codes for {commodity_name}:")
        for s in successful:
            print(f"  Code {s['code']}: {s['url']}")
    else:
        print(f"\n✗ No working codes found for {commodity_name}")
        
    return results

# Main test function
def main():
    print("PDF Commodity Verification Script")
    print("=" * 40)
    
    # Install required packages if not available
    try:
        import pdfplumber
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "pdfplumber", "requests"])
        import pdfplumber
    
    # Test cases based on our analysis and the examples provided
    test_cases = [
        {
            "name": "Barite",
            "url_name": "barite",
            "codes": ["05", "08"],  # Current mapping vs example
            "year": "97"
        },
        {
            "name": "Kyanite",
            "url_name": "kyanite",
            "codes": ["29"],  # Current mapping
            "year": "97"
        },
        {
            "name": "Fluorspar",
            "url_name": "fluorspar",
            "codes": ["17"],  # Current mapping
            "year": "97"
        }
    ]
    
    all_results = []
    
    for test_case in test_cases:
        results = test_multiple_codes(
            test_case["name"], 
            test_case["url_name"], 
            test_case["codes"], 
            test_case["year"]
        )
        all_results.extend(results)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    successful = [r for r in all_results if r["success"]]
    print(f"Successful verifications: {len(successful)}")
    
    for s in successful:
        print(f"  ✓ Code {s['code']} for {s['url'].split('/')[-2]}")
        
    print(f"\nFailed verifications: {len(all_results) - len(successful)}")

if __name__ == "__main__":
    main()