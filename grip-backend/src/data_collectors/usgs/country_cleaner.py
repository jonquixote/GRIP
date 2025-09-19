#!/usr/bin/env python3
"""
Comprehensive Country Name Cleaner for USGS Mineral Data

This script cleans and standardizes country names in USGS mineral commodity data files.
It consolidates duplicate entries, fixes common parsing errors, and standardizes
country names to ensure data consistency.

Usage:
    python3 country_cleaner.py [data_directory]
    
    If no directory specified, defaults to 'comprehensive_data'
"""

import json
import os
import sys
import re
from collections import Counter

# Comprehensive country name correction and consolidation mapping
COUNTRY_CLEANING_MAP = {
    # Partial names and obvious corrections
    'Chil': 'Chile',
    'Franc': 'France',
    'Greec': 'Greece',
    'Mozambiqu': 'Mozambique',
    'Sierra Leon': 'Sierra Leone',
    'Zair': 'Zaire',
    
    # Country names with extra technical text
    'Australia not available Th': 'Australia',
    'Canada not available Th': 'Canada',
    'China (andalusite': 'China',
    'China China Kyrgyzstan and Peru ar': 'China',
    'China Larg': 'China',
    'China Zinc chapter for zinc reserves': 'China',
    'China and Peru': 'China',
    'China germanium': 'China',
    'China ores ar': 'China',
    'Germany ( ( ( (': 'Germany',
    'Germany Zinc chapter for zinc reserves': 'Germany',
    'Germany compounds': 'Germany',
    'Germany countries:': 'Germany',
    'Germany country to which th': 'Germany',
    'Germany produced sulfur production may not b': 'Germany',
    'India (kyanit': 'India',
    'India Larg': 'India',
    'India Moderat': 'India',
    'India attributed For instanc': 'India',
    'India country for which th': 'India',
    'India country to which th': 'India',
    'India of aluminosilicates': 'India',
    'India processed long distances from wher': 'India',
    'India reserves wer': 'India',
    'India wher': 'India',
    'Iran Arabian oil may b': 'Iran',
    'Iran attributed For instanc': 'Iran',
    'Iran may not b': 'Iran',
    'Iran sulfur from Saudi Arabian oil may b': 'Iran',
    'Iran they ar': 'Iran',
    'Italy ( ( ( (': 'Italy',
    'Italy Arabian oil may b': 'Italy',
    'Italy Reserves': 'Italy',
    'Italy Reserves and reserv': 'Italy',
    'Italy may not b': 'Italy',
    'Japan about%': 'Japan',
    'Japan countries:': 'Japan',
    'Japan producing countries but data': 'Japan',
    'Japan production': 'Japan',
    'Japan recovered at refineries in th': 'Japan',
    'Japan reserves wer': 'Japan',
    'Japan wher': 'Japan',
    'Jordan NA Larg': 'Jordan',
    'Kazakhstan concentrat': 'Kazakhstan',
    'Kazakhstan for zinc reserves': 'Kazakhstan',
    'Kazakhstan long distances from wher': 'Kazakhstan',
    'Kazakhstan may not b': 'Kazakhstan',
    'Kazakhstan production': 'Kazakhstan',
    'Kazakhstan sulfur from Saudi Arabian oil may b': 'Kazakhstan',
    'Kazakhstan unspecified': 'Kazakhstan',
    'Kazakhstan which had been a leading producer in did not produc': 'Kazakhstan',
    'Kyrgyzstan China Kyrgyzstan and Peru': 'Kyrgyzstan',
    'Kyrgyzstan China Kyrgyzstan and Peru ar': 'Kyrgyzstan',
    'Mexico (exports': 'Mexico',
    'Mexico (net exports': 'Mexico',
    'Mexico (net exports hav': 'Mexico',
    'Mexico (net exports reserves': 'Mexico',
    'Mexico attributed For instanc': 'Mexico',
    'Mexico for most ar': 'Mexico',
    'Mexico producing countries': 'Mexico',
    'Netherlands Arabian oil may b': 'Netherlands',
    'Peru (andalusite': 'Peru',
    'Peru (exports reserves': 'Peru',
    'Peru crud': 'Peru',
    'Poland data ar': 'Poland',
    'Poland recovered at refineries in th': 'Poland',
    'Qatar Larg': 'Qatar',
    'Russia Moderat': 'Russia',
    'Russia datolit': 'Russia',
    'Russia ores ar': 'Russia',
    'South Africa (andalusite': 'South Africa',
    'South Africa sillimanite': 'South Africa',
    'Spain (includes pegmatites': 'Spain',
    'Turkey concentrat': 'Turkey',
    'Turkey refined borates': 'Turkey',
    'United States (from Cliffsid': 'United States',
    'United States (kyanite Larg': 'United States',
    'United States Previously published': 'United States',
    'United States Reserves of sulfur in crud': 'United States',
    'United States Significant in th': 'United States',
    'United States World primary gallium production capacity in was estimated': 'United States',
    'United States World primary gallium production capacity in was estimated to b': 'United States',
    'World total (rounded *': 'World total',
    'World total (rounded Larg': 'World total',
    'World total (rounded XX XX XX': 'World total',
    
    # Consolidation of country variants
    'Brazil Moderat': 'Brazil',
    'Brazil demand': 'Brazil',
    'Canada countries': 'Canada',
    'Canada processing': 'Canada',
    'Canada production is a result of th': 'Canada',
    'Finland foreseeabl': 'Finland',
    'Finland long distances from wher': 'Finland',
    'Israel NA Larg': 'Israel',
    'Kuwait country for which th': 'Kuwait',
    'Kuwait sulfur from Saudi Arabian oil may b': 'Kuwait',
    'Morocco production': 'Morocco',
    'Norway reserves': 'Norway',
    
    # Special category consolidation
    'Other': 'Other countries',
    'Other PGMs': 'Other countries',
    'approximately million tons to tons Finland is th': 'Finland',
    'of Korea and Russia Refined gallium production in was estimated to b': 'South Korea',
    'other % Platinum: South Africa %; Germany %; Italy %; Switzerland %; and other %': 'Other countries',
    'Platinum: South Africa %; Belgium %; Germany %; Italy %; and other %': 'Other countries',
    'Platinum: South Africa %; Germany %; Italy %; Russia %; and other %': 'Other countries',
    'Platinum: South Africa %; Germany %; Switzerland %; Italy %; and other %': 'Other countries',
    'Platinum: South Africa %; Switzerland %; Germany %; Belgium %; and other %': 'Other countries',
    
    # Alternative names and corrections
    'Burma': 'Myanmar',
    'Côte d’Ivoire': 'Ivory Coast',
    'Cote d\'Ivoire': 'Ivory Coast',
    'Czech Republic': 'Czechia',
    'Korea Republic': 'South Korea',
    'Korea Republic of': 'South Korea',
    'Korea North': 'North Korea',
    'UK': 'United Kingdom',
    'US': 'United States',
    'USA': 'United States',
    'Argentinae': 'Argentina',
    'Azerbaijane': 'Azerbaijan',
    'Namibiae': 'Namibia',
    'Russiae': 'Russia',
    
    # Additional patterns to clean up
    'Austria   ()': 'Austria',
    'Brazil (crude)': 'Brazil',
    'Bulgaria   ()': 'Bulgaria',
    'Canada   ()': 'Canada',
    'Canada   () ()': 'Canada',
    'China   () ()': 'China',
    'France   () ()': 'France',
    'Germany   ()': 'Germany',
    'India   ()': 'India',
    'India   () ()': 'India',
    'Israel   ()': 'Israel',
    'Israel   () ()': 'Israel',
    'Italy   () ()': 'Italy',
    'Japan   ()': 'Japan',
    'Japan   () ()': 'Japan',
    'Portugal   ()': 'Portugal',
    'Spain   ()': 'Spain',
    'Sweden   ()': 'Sweden',
    'Thailand   ()': 'Thailand',
    'Turkey   ()': 'Turkey',
    'United Kingdom   ()': 'United Kingdom',
    'United States   ()': 'United States',
    'Zimbabwe   ()': 'Zimbabwe',
    
    # More malformed entries
    'Austria —  ()': 'Austria',
    'Belgium   ()': 'Belgium',
    'Germany  — ()': 'Germany',
    'India . . ()': 'India',
    'Israel . . ()': 'Israel',
    'Italy . . ()': 'Italy',
    'Japan . . ()': 'Japan',
    'Jordan   ()': 'Jordan',
    'Norway   ()': 'Norway',
    'Osmium    () —': 'Osmium',
    'Osmium  ()   —': 'Osmium',
    'Osmium ()': 'Osmium',
    'Peru (export': 'Peru',
    'Spain ()': 'Spain',
    'Turkey   ()': 'Turkey',
    'Ukraine   ()': 'Ukraine',
    
    # Truncated entries
    'Other countrie': 'Other countries',
    'Congo (Kinshasa': 'Congo (Kinshasa)',
    'Zimbabw': 'Zimbabwe',
    'Ukrain': 'Ukraine',
    
    # Consolidate all "World total" variants
    'World total': 'World',
    'World total (may be rounded)': 'World',
    'World total (rounded)': 'World',
    'World total World total': 'World',
    'World total (rounded)   Larg': 'World',
    
    # Consolidate various "Other" representations
    'Other countries': 'Other',
    'Other country': 'Other',
    'Other nations': 'Other',
    'Rest of world': 'Other',
    'Others': 'Other',
    'Remaining countries': 'Other',
    'Various countries': 'Other',
    'Several countries': 'Other',
    'Other countries   NA': 'Other',
    
    # Fix partial country names
    'Chilean': 'Chile',
    'Australian': 'Australia',
    'Canadian': 'Canada',
    'Chinese': 'China',
    'German': 'Germany',
    'Indian': 'India',
    'Japanese': 'Japan',
    'Mexican': 'Mexico',
    'Russian': 'Russia',
    'American': 'United States',
    'US ': 'United States',
    'USA ': 'United States',
    'UK ': 'United Kingdom',
    
    # Special characters and malformed entries
    '(=) . . . .': 'Unknown',
    '(=) . . . . .': 'Unknown',
    '.. .% .% .% %.': 'Unknown',
    '.. .% .%.': 'Unknown',
    '.. .% Free .%.': 'Unknown',
    'e': 'Unknown',
    'Rhodium': 'Other',
    'Palladium': 'Other',
    'Platinum': 'Other',
}

def clean_country_name(country):
    """
    Clean and standardize a country name using the comprehensive mapping
    
    Args:
        country (str): Original country name
        
    Returns:
        str: Cleaned and standardized country name
    """
    if not country or not isinstance(country, str):
        return country
    
    # Remove extra whitespace
    country = country.strip()
    
    # Remove trailing special characters and parentheses
    country = re.sub(r'[\s()]*$', '', country)
    country = re.sub(r'^[\s()]*', '', country)
    
    # Remove special character patterns at the end
    country = re.sub(r'\s+[()]*\s*$', '', country)
    
    # Remove patterns like "   ()" or "   () ()"
    country = re.sub(r'\s*\(\s*\)\s*$', '', country)
    country = re.sub(r'\s*\(\s*\)\s*\(\s*\)\s*$', '', country)
    
    # Remove percentage patterns and dots
    country = re.sub(r'[\d.]*\s*%', '', country)
    country = re.sub(r'\s*\.\s*%\s*', '', country)
    country = re.sub(r'\s*\.\s*\.\s*', '', country)
    
    # Remove trailing dashes and other special characters
    country = re.sub(r'\s*[—–-]+\s*$', '', country)
    
    # Remove "NA" at the end
    country = re.sub(r'\s+NA\s*$', '', country)
    
    # Truncate excessively long country names that are likely malformed
    if len(country) > 50:
        country = country[:50]
    
    # Apply the cleaning mapping
    if country in COUNTRY_CLEANING_MAP:
        country = COUNTRY_CLEANING_MAP[country]
    
    return country

def clean_data_file(filepath):
    """
    Clean country names in a JSON data file
    
    Args:
        filepath (str): Path to the JSON data file
        
    Returns:
        tuple: (records_processed, corrections_made)
    """
    try:
        # Read the data
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Process each record
        corrections_made = 0
        records_processed = len(data)
        
        for record in data:
            if 'country' in record:
                original_country = record['country']
                cleaned_country = clean_country_name(original_country)
                if original_country != cleaned_country:
                    record['country'] = cleaned_country
                    corrections_made += 1
        
        # Write the cleaned data back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return records_processed, corrections_made
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0, 0

def clean_comprehensive_data(data_directory='../../../data/usgs'):
    """
    Clean all JSON data files in the comprehensive data directory
    
    Args:
        data_directory (str): Path to the data directory
        
    Returns:
        dict: Summary of cleaning results
    """
    if not os.path.exists(data_directory):
        print(f"Directory {data_directory} does not exist")
        return {}
    
    # Get all JSON files in the directory (excluding collection_summary.json)
    json_files = [f for f in os.listdir(data_directory) if f.endswith('.json') and f != 'collection_summary.json']
    
    if not json_files:
        print(f"No JSON data files found in {data_directory}")
        return {}
    
    print(f"Cleaning country names in {len(json_files)} data files...")
    print("=" * 60)
    
    total_records = 0
    total_corrections = 0
    files_processed = 0
    
    for filename in json_files:
        filepath = os.path.join(data_directory, filename)
        records, corrections = clean_data_file(filepath)
        
        if records > 0:
            total_records += records
            total_corrections += corrections
            files_processed += 1
            
            if corrections > 0:
                print(f"{filename:40} | Records: {records:4d} | Corrections: {corrections:3d}")
    
    # Summary
    print("=" * 60)
    print(f"SUMMARY:")
    print(f"  Files processed:     {files_processed}")
    print(f"  Total records:       {total_records:,}")
    print(f"  Total corrections:   {total_corrections:,}")
    print(f"  Average corrections: {total_corrections/files_processed if files_processed > 0 else 0:.1f} per file")
    
    return {
        'files_processed': files_processed,
        'total_records': total_records,
        'total_corrections': total_corrections
    }

def analyze_country_names(data_directory='../../../data/usgs'):
    """
    Analyze the current state of country names in the data
    
    Args:
        data_directory (str): Path to the data directory
        
    Returns:
        dict: Analysis results including unique country count and top countries
    """
    if not os.path.exists(data_directory):
        print(f"Directory {data_directory} does not exist")
        return {}
    
    # Get all JSON files in the directory (excluding collection_summary.json)
    json_files = [f for f in os.listdir(data_directory) if f.endswith('.json') and f != 'collection_summary.json']
    
    all_countries = []
    
    for filename in json_files:
        filepath = os.path.join(data_directory, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for record in data:
                if 'country' in record:
                    all_countries.append(record['country'])
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    
    # Count unique countries
    country_counts = Counter(all_countries)
    unique_countries = sorted(list(country_counts.keys()))
    
    # Print more detailed analysis
    print(f"Total country entries: {len(all_countries)}")
    print(f"Unique countries: {len(unique_countries)}")
    print("\nTop 20 countries by count:")
    for country, count in country_counts.most_common(20):
        print(f"  {country}: {count}")
    
    # Show some of the problematic countries
    print("\nSample of countries with partial names or issues:")
    problematic = [country for country in unique_countries if len(country) < 15 and ('(' in country or ':' in country or ';' in country or '%' in country)]
    for country in list(problematic)[:20]:
        print(f"  {country}")
    
    return {
        'total_records': len(all_countries),
        'unique_countries': len(unique_countries),
        'country_counts': country_counts,
        'unique_country_list': unique_countries
    }

def main():
    """Main function to run the country cleaner"""
    # Check for analysis-only flag
    if len(sys.argv) > 1 and sys.argv[1] == '--analyze-only':
        data_directory = '../../../data/usgs' if len(sys.argv) < 3 else sys.argv[2]
        print(f"GRIP Country Name Analyzer")
        print(f"Data directory: {data_directory}")
        print()
        
        # Analyze current state
        print("Analyzing current country names...")
        analysis_before = analyze_country_names(data_directory)
        if 'unique_countries' not in analysis_before:
            print("Failed to analyze data directory")
            return
        print(f"Before cleaning: {analysis_before['unique_countries']} unique countries")
        return
    
    # Check for test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        data_directory = '.'  # Use current directory for test
        print(f"GRIP Country Name Cleaner - Test Mode")
        print(f"Data directory: {data_directory}")
        print()
        
        # Analyze current state
        print("Analyzing current country names...")
        analysis_before = analyze_country_names(data_directory)
        if 'unique_countries' not in analysis_before:
            print("Failed to analyze data directory")
            return
        print(f"Before cleaning: {analysis_before['unique_countries']} unique countries")
        print()
        
        # Clean the data
        results = clean_comprehensive_data(data_directory)
        
        if results:
            print()
            
            # Analyze after cleaning
            print("Analyzing country names after cleaning...")
            analysis_after = analyze_country_names(data_directory)
            print(f"After cleaning: {analysis_after['unique_countries']} unique countries")
            print()
            
            # Show improvement
            reduction = analysis_before['unique_countries'] - analysis_after['unique_countries']
            reduction_percent = (reduction / analysis_before['unique_countries']) * 100 if analysis_before['unique_countries'] > 0 else 0
            print(f"IMPROVEMENT:")
            print(f"  Countries reduced: {reduction} ({reduction_percent:.1f}%)")
            print(f"  Data preserved:    {analysis_after['total_records']:,} records")
            print()
            
            # Show top countries
            print("Top 10 countries after cleaning:")
            print("-" * 40)
            for country, count in analysis_after['country_counts'].most_common(10):
                print(f"{country:25} {count:5,}")
        return
    
    # Get data directory from command line or use default
    data_directory = sys.argv[1] if len(sys.argv) > 1 else '../../../data/usgs'
    
    print(f"GRIP Country Name Cleaner")
    print(f"Data directory: {data_directory}")
    print()
    
    # Analyze current state
    print("Analyzing current country names...")
    analysis_before = analyze_country_names(data_directory)
    if 'unique_countries' not in analysis_before:
        print("Failed to analyze data directory")
        return
    print(f"Before cleaning: {analysis_before['unique_countries']} unique countries")
    print()
    
    # Clean the data
    results = clean_comprehensive_data(data_directory)
    
    if results:
        print()
        
        # Analyze after cleaning
        print("Analyzing country names after cleaning...")
        analysis_after = analyze_country_names(data_directory)
        print(f"After cleaning: {analysis_after['unique_countries']} unique countries")
        print()
        
        # Show improvement
        reduction = analysis_before['unique_countries'] - analysis_after['unique_countries']
        reduction_percent = (reduction / analysis_before['unique_countries']) * 100 if analysis_before['unique_countries'] > 0 else 0
        print(f"IMPROVEMENT:")
        print(f"  Countries reduced: {reduction} ({reduction_percent:.1f}%)")
        print(f"  Data preserved:    {analysis_after['total_records']:,} records")
        print()
        
        # Show top countries
        print("Top 10 countries after cleaning:")
        print("-" * 40)
        for country, count in analysis_after['country_counts'].most_common(10):
            print(f"{country:25} {count:5,}")

if __name__ == "__main__":
    main()