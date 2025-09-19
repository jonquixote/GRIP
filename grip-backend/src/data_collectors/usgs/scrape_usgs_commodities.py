#!/usr/bin/env python3
"""
Script to scrape USGS commodity statistics page and extract all commodities with their links
"""
import requests
from bs4 import BeautifulSoup
import json
import re
import sys

def scrape_usgs_commodities():
    """Scrape USGS commodity statistics page and extract all commodities"""
    url = "https://www.usgs.gov/centers/national-minerals-information-center/commodity-statistics-and-information"
    
    try:
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content area
        content_div = soup.find('div', class_='content')
        if not content_div:
            content_div = soup.find('main') or soup.find('div', role='main')
        
        commodities = []
        
        # Look for lists of commodities
        lists = content_div.find_all(['ul', 'ol']) if content_div else []
        
        for list_elem in lists:
            items = list_elem.find_all('li')
            for item in items:
                # Extract text and links
                text = item.get_text(strip=True)
                links = item.find_all('a', href=True)
                
                if links:
                    # Handle special cases with multiple links in one entry
                    if len(links) > 1 or ('(' in text and ')' in text):
                        # Parse special cases like "Granite (Crushed Stone, Dimension Stone)"
                        # Extract the main name and sub-items
                        match = re.search(r'^(.*?)\\s*\\(([^)]+)\\)', text)
                        if match:
                            main_name = match.group(1).strip()
                            sub_items = match.group(2).split(',')
                            
                            # Create separate entries for each sub-item
                            for i, link in enumerate(links):
                                if i < len(sub_items):
                                    sub_name = sub_items[i].strip()
                                    full_name = f"{main_name} {sub_name}"
                                else:
                                    full_name = f"{main_name} {i+1}"
                                
                                href = link['href']
                                if href.startswith('/'):
                                    href = f"https://www.usgs.gov{href}"
                                
                                # Extract url_name from the link
                                url_match = re.search(r'centers/([^/]+)-statistics-and-information', href)
                                url_name = url_match.group(1) if url_match else full_name.lower().replace(' ', '-')
                                
                                commodities.append({
                                    "name": full_name,
                                    "url_name": url_name,
                                    "link": href
                                })
                        else:
                            # Handle multiple links without parentheses
                            for link in links:
                                href = link['href']
                                if href.startswith('/'):
                                    href = f"https://www.usgs.gov{href}"
                                
                                link_text = link.get_text(strip=True)
                                # Extract url_name from the link
                                url_match = re.search(r'centers/([^/]+)-statistics-and-information', href)
                                url_name = url_match.group(1) if url_match else link_text.lower().replace(' ', '-')
                                
                                commodities.append({
                                    "name": link_text,
                                    "url_name": url_name,
                                    "link": href
                                })
                    else:
                        # Handle single link entries
                        link = links[0]
                        href = link['href']
                        if href.startswith('/'):
                            href = f"https://www.usgs.gov{href}"
                        
                        link_text = link.get_text(strip=True)
                        # Use the text as name, but if it's generic, use the main item text
                        if link_text.lower() in ['statistics and information', 'more information']:
                            name = text.split('(')[0].strip() if '(' in text else text
                        else:
                            name = link_text
                        
                        # Extract url_name from the link
                        url_match = re.search(r'centers/([^/]+)-statistics-and-information', href)
                        url_name = url_match.group(1) if url_match else name.lower().replace(' ', '-')
                        
                        commodities.append({
                            "name": name,
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
        print(f"Error scraping USGS commodities: {e}")
        return []

def main():
    """Main function to scrape and save commodities"""
    print("Scraping USGS commodity statistics page...")
    commodities = scrape_usgs_commodities()
    
    if commodities:
        # Save to JSON file
        with open('usgs_commodities.json', 'w') as f:
            json.dump(commodities, f, indent=2)
        
        print(f"Successfully extracted {len(commodities)} commodities")
        print("Saved to usgs_commodities.json")
        
        # Show sample data
        print("\nSample entries:")
        for i, commodity in enumerate(commodities[:10]):
            print(f"  {i+1}. {commodity['name']} -> {commodity['url_name']} ({commodity['link']})")
        
        # Show special cases
        print("\nSpecial cases (with spaces in url_name):")
        special_cases = [c for c in commodities if ' ' in c['url_name']]
        for commodity in special_cases[:5]:
            print(f"  - {commodity['name']} -> {commodity['url_name']}")
    else:
        print("No commodities found")

if __name__ == "__main__":
    main()