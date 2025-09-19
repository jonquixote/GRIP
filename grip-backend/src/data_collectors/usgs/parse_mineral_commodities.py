#!/usr/bin/env python3
"""
Script to parse USGS commodity statistics page and extract only mineral commodities with their links
"""
import requests
from bs4 import BeautifulSoup
import json
import re

def extract_commodity_section(content):
    """Extract only the commodity section from the page content"""
    # Look for the section with commodity listings
    # Find the "Nonfuel Minerals" heading and extract content until the next major section
    lines = content.split('\n')
    commodity_lines = []
    in_commodity_section = False
    
    for line in lines:
        if '<h2><strong>Nonfuel Minerals</strong></h2>' in line:
            in_commodity_section = True
            continue
        elif in_commodity_section:
            if '<h2>' in line and 'Nonfuel Minerals' not in line:
                # We've reached the end of the commodity section
                break
            commodity_lines.append(line)
    
    return '\n'.join(commodity_lines)

def parse_usgs_commodities():
    """Parse USGS commodity statistics page and extract only mineral commodities"""
    url = "https://www.usgs.gov/centers/national-minerals-information-center/commodity-statistics-and-information"
    
    try:
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        
        # Extract only the commodity section
        commodity_section = extract_commodity_section(content)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(commodity_section, 'html.parser')
        
        # Find all list items containing commodity links
        commodities = []
        
        # Look for all <li> elements
        list_items = soup.find_all('li')
        
        for item in list_items:
            links = item.find_all('a', href=True)
            if links:
                text = item.get_text(strip=True)
                
                # Handle special cases like "Granite (Crushed Stone, Dimension Stone)"
                if '(' in text and ')' in text and len(links) > 1:
                    # Extract the main name and sub-items
                    # Look for pattern like "Granite (Crushed Stone, Dimension Stone)"
                    match = re.search(r'^([^(\n]+)\s*\(([^)]+)\)', text)
                    if match:
                        main_name = match.group(1).strip()
                        sub_items = [s.strip() for s in match.group(2).split(',')]
                        
                        # Create separate entries for each link
                        for i, link in enumerate(links):
                            if i < len(sub_items):
                                sub_name = sub_items[i]
                                full_name = f"{main_name} {sub_name}"
                            else:
                                full_name = f"{main_name} Link {i+1}"
                            
                            href = link['href']
                            if href.startswith('/'):
                                href = f"https://www.usgs.gov{href}"
                            
                            # Extract url_name from the link
                            url_match = re.search(r'centers/([^/]+)-statistics-and-information', href)
                            url_name = url_match.group(1) if url_match else full_name.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')
                            
                            commodities.append({
                                "name": full_name,
                                "url_name": url_name,
                                "link": href
                            })
                else:
                    # Handle single link cases
                    for link in links:
                        href = link['href']
                        if href.startswith('/'):
                            href = f"https://www.usgs.gov{href}"
                        
                        link_text = link.get_text(strip=True)
                        
                        # Extract url_name from the link - this is the critical part
                        url_match = re.search(r'centers/([^/]+)-statistics-and-information', href)
                        if url_match:
                            url_name = url_match.group(1)
                            commodities.append({
                                "name": link_text,
                                "url_name": url_name,
                                "link": href
                            })
        
        # Remove duplicates while preserving order
        seen = set()
        unique_commodities = []
        for commodity in commodities:
            identifier = (commodity['name'], commodity['url_name'])
            if identifier not in seen:
                seen.add(identifier)
                unique_commodities.append(commodity)
        
        return unique_commodities
        
    except Exception as e:
        print(f"Error parsing USGS commodities: {e}")
        return []

def main():
    """Main function to parse and save commodities"""
    print("Parsing USGS commodity statistics page...")
    commodities = parse_usgs_commodities()
    
    if commodities:
        # Save to JSON file
        with open('usgs_mineral_commodities.json', 'w') as f:
            json.dump(commodities, f, indent=2)
        
        print(f"Successfully extracted {len(commodities)} mineral commodities")
        print("Saved to usgs_mineral_commodities.json")
        
        # Show sample data
        print("\nSample entries:")
        for i, commodity in enumerate(commodities[:20]):
            print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']} ({commodity['link']})")
        
        # Show special cases
        special_cases = [c for c in commodities if ' ' in c['name'] and ('Crushed Stone' in c['name'] or 'Dimension Stone' in c['name'])]
        print(f"\nSpecial cases found: {len(special_cases)}")
        for i, commodity in enumerate(special_cases):
            print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']}")
    else:
        print("No commodities found")

if __name__ == "__main__":
    main()