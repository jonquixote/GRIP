#!/usr/bin/env python3
"""
Test script to debug PDF parsing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.data_collectors.usgs_collector import USGSCollector

def test_pdf_parsing():
    """Test PDF parsing for aluminum in 2020"""
    print("Testing PDF parsing for aluminum in 2020...")
    
    # Initialize collector
    collector = USGSCollector()
    
    # Test parsing the aluminum PDF
    pdf_url = "https://pubs.usgs.gov/periodicals/mcs2020/mcs2020-aluminum.pdf"
    commodity = "aluminum"
    year = 2020
    
    print(f"Parsing PDF: {pdf_url}")
    
    # Parse the PDF
    parsed_data = collector._parse_mineral_commodity_summary_pdf(pdf_url, commodity, year)
    
    print(f"Parsing result: {parsed_data}")
    
    # Test parsing the copper PDF
    print("\nTesting PDF parsing for copper in 2020...")
    pdf_url = "https://pubs.usgs.gov/periodicals/mcs2020/mcs2020-copper.pdf"
    commodity = "copper"
    year = 2020
    
    print(f"Parsing PDF: {pdf_url}")
    
    # Parse the PDF
    parsed_data = collector._parse_mineral_commodity_summary_pdf(pdf_url, commodity, year)
    
    print(f"Parsing result: {parsed_data}")
    
    # Test the multiplier extraction directly
    print("\nTesting multiplier extraction directly...")
    # Simulate a page text with "(Data in metric tons"
    test_text_1 = "ALUMINUM\n(Data in metric tons of usable ore, unless otherwise noted)"
    multiplier_1 = collector._extract_multiplier(test_text_1)
    print(f"Multiplier for '(Data in metric tons': {multiplier_1}")
    
    # Simulate a page text with "(Data in thousands of metric tons"
    test_text_2 = "COPPER\n(Data in thousands of metric tons of usable ore, unless otherwise noted)"
    multiplier_2 = collector._extract_multiplier(test_text_2)
    print(f"Multiplier for '(Data in thousands of metric tons': {multiplier_2}")
    
    # Simulate a page text with "(Data in million metric tons"
    test_text_3 = "GOLD\n(Data in million metric tons of usable ore, unless otherwise noted)"
    multiplier_3 = collector._extract_multiplier(test_text_3)
    print(f"Multiplier for '(Data in million metric tons': {multiplier_3}")
    
    # Simulate a page text with "(Data in billion metric tons"
    test_text_4 = "LITHIUM\n(Data in billion metric tons of lithium content, unless otherwise noted)"
    multiplier_4 = collector._extract_multiplier(test_text_4)
    print(f"Multiplier for '(Data in billion metric tons': {multiplier_4}")

if __name__ == "__main__":
    test_pdf_parsing()