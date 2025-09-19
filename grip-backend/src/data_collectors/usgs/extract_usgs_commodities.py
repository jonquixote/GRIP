#!/usr/bin/env python3
"""
Script to extract USGS commodity statistics and information.

This script parses a pre-fetched HTML file containing the USGS commodity statistics page
and extracts all commodity names and their links. For entries with multiple links 
(like "Granite (Crushed Stone, Dimension Stone)"), it creates separate entries for each link.

The script extracts the text between "centers/" and "-statistics-and-information" from each 
link URL as this is the name needed for URLs.

Results are saved to a JSON file with the structure:
[{"name": "commodity_name", "url_name": "url_part", "link": "full_url"}, ...]
"""
import re
import json
import sys
import os

def extract_commodities_from_html(html_content):
    """Extract all commodities from the HTML content"""
    # Find all standard commodity links: <li><a href="...">Name</a></li>
    standard_pattern = r'<li><a href="(/centers/[^"]*-statistics-and-information)">([^<]+)</a></li>'
    standard_matches = re.findall(standard_pattern, html_content)
    
    print(f"Found {len(standard_matches)} standard commodity matches")
    
    # Create commodity entries for standard matches
    commodities = []
    for href, name in standard_matches:
        # Extract the url_name from the href
        # Pattern: extract the part between the last "/" and "-statistics-and-information"
        url_match = re.search(r'/centers/.*?/([^/]+)-statistics-and-information', href)
        if url_match:
            url_name = url_match.group(1)
            
            commodity_entry = {
                "name": name.strip(),
                "url_name": url_name,
                "link": f"https://www.usgs.gov{href}"
            }
            commodities.append(commodity_entry)
    
    # Find special cases with multiple links in one line
    # Pattern: <li>Text (<a href="...">Text1</a>, <a href="...">Text2</a>)</li>
    special_pattern = r'<li>([^<(]+)\(<a href="(/centers/[^"]*-statistics-and-information)">([^<]+)</a>,\s*<a href="(/centers/[^"]*-statistics-and-information)">([^<]+)</a>\)\s*</li>'
    special_matches = re.findall(special_pattern, html_content)
    
    print(f"Found {len(special_matches)} special case matches")
    
    # Handle special cases
    for main_name, href1, sub1, href2, sub2 in special_matches:
        main_name = main_name.strip()
        # Remove &nbsp; if present
        main_name = main_name.replace('&nbsp;', '').strip()
        
        # Extract url names
        url_match1 = re.search(r'/centers/.*?/([^/]+)-statistics-and-information', href1)
        url_match2 = re.search(r'/centers/.*?/([^/]+)-statistics-and-information', href2)
        
        if url_match1 and url_match2:
            url_name1 = url_match1.group(1)
            url_name2 = url_match2.group(1)
            
            # Add the first sub-commodity
            commodity_entry1 = {
                "name": f"{main_name} {sub1.strip()}",
                "url_name": url_name1,
                "link": f"https://www.usgs.gov{href1}"
            }
            commodities.append(commodity_entry1)
            
            # Add the second sub-commodity
            commodity_entry2 = {
                "name": f"{main_name} {sub2.strip()}",
                "url_name": url_name2,
                "link": f"https://www.usgs.gov{href2}"
            }
            commodities.append(commodity_entry2)
    
    print(f"Total commodities: {len(commodities)}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_commodities = []
    for item in commodities:
        # Create a unique identifier based on name and url_name
        identifier = (item["name"], item["url_name"])
        if identifier not in seen:
            seen.add(identifier)
            unique_commodities.append(item)
    
    print(f"Total unique commodities: {len(unique_commodities)}")
    
    return unique_commodities

def save_to_json(commodities, filename="usgs_commodities.json"):
    """Save commodities data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(commodities, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(commodities)} commodities to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to JSON file: {e}")
        return False

def main():
    """Main function to run the extractor"""
    print("Extracting USGS commodity statistics...")
    
    # Check if HTML file is provided as argument
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    else:
        html_file = "debug_page.html"
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: HTML file '{html_file}' not found.")
        print("Please provide the path to the HTML file as an argument.")
        sys.exit(1)
    
    # Read the HTML file
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        sys.exit(1)
    
    # Extract commodities
    commodities = extract_commodities_from_html(html_content)
    
    if not commodities:
        print("No commodities found.")
        sys.exit(1)
    
    # Display some statistics
    print(f"Found {len(commodities)} unique commodity entries.")
    
    # Show first few entries as sample
    print("\nSample entries:")
    for i, commodity in enumerate(commodities[:10]):
        print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']}")
    
    # Show special case examples
    print("\nSpecial case examples:")
    special_cases = [c for c in commodities if 'Granite' in c['name'] or 'Limestone' in c['name'] or 'Marble' in c['name'] or 'Sandstone' in c['name'] or 'Slate' in c['name']]
    for i, commodity in enumerate(special_cases[:10]):
        print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']}")
    
    # Save to JSON file
    output_file = "usgs_commodities.json"
    if save_to_json(commodities, output_file):
        print(f"\nData saved to {os.path.abspath(output_file)}")
    else:
        print("Failed to save data to JSON file.")
        sys.exit(1)

if __name__ == "__main__":
    main()