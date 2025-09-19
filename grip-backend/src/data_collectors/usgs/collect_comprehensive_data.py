#!/usr/bin/env python3
"""
Final comprehensive USGS data collection script
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from data_collectors.usgs_collector import USGSCollector

def collect_comprehensive_usgs_data():
    """Collect comprehensive USGS data for all working commodities"""
    
    # High-value commodities that we know work well
    working_commodities = [
        {"name": "Gold", "url_name": "gold", "category": "Precious Metals"},
        {"name": "Silver", "url_name": "silver", "category": "Precious Metals"},
        {"name": "Copper", "url_name": "copper", "category": "Base Metals"},
        {"name": "Aluminum", "url_name": "aluminum", "category": "Base Metals"},
        {"name": "Lead", "url_name": "lead", "category": "Base Metals"},
        {"name": "Zinc", "url_name": "zinc", "category": "Base Metals"},
        {"name": "Nickel", "url_name": "nickel", "category": "Base Metals"},
        {"name": "Tin", "url_name": "tin", "category": "Base Metals"},
        {"name": "Cobalt", "url_name": "cobalt", "category": "Critical Minerals"},
        {"name": "Lithium", "url_name": "lithium", "category": "Critical Minerals"},
        {"name": "Graphite", "url_name": "graphite", "category": "Critical Minerals"},
        {"name": "Tungsten", "url_name": "tungsten", "category": "Critical Minerals"},
        {"name": "Titanium", "url_name": "titanium", "category": "Critical Minerals"},
        {"name": "Uranium", "url_name": "uranium", "category": "Energy Minerals"},
        {"name": "Platinum", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Palladium", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Rhodium", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Iridium", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Osmium", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Ruthenium", "url_name": "platinum", "category": "Precious Metals"},
        {"name": "Rare Earths", "url_name": "rare_earths", "category": "Critical Minerals"},
        {"name": "Indium", "url_name": "indium", "category": "Technology Minerals"},
        {"name": "Gallium", "url_name": "gallium", "category": "Technology Minerals"},
        {"name": "Germanium", "url_name": "germanium", "category": "Technology Minerals"},
        {"name": "Silicon", "url_name": "silicon", "category": "Technology Minerals"},
        {"name": "Antimony", "url_name": "antimony", "category": "Technology Minerals"},
        {"name": "Bismuth", "url_name": "bismuth", "category": "Technology Minerals"},
        {"name": "Tantalum", "url_name": "tantalum", "category": "Technology Minerals"},
        {"name": "Niobium", "url_name": "niobium", "category": "Technology Minerals"},
        {"name": "Vanadium", "url_name": "vanadium", "category": "Technology Minerals"},
        {"name": "Molybdenum", "url_name": "molybdenum", "category": "Technology Minerals"},
        {"name": "Chromium", "url_name": "chromium", "category": "Technology Minerals"},
        {"name": "Manganese", "url_name": "manganese", "category": "Technology Minerals"},
        {"name": "Iron Ore", "url_name": "iron_ore", "category": "Base Metals"},
        {"name": "Steel", "url_name": "iron_and_steel", "category": "Base Metals"},
        {"name": "Magnesium", "url_name": "magnesium", "category": "Light Metals"},
        {"name": "Calcium", "url_name": "calcium", "category": "Industrial Minerals"},
        {"name": "Phosphate", "url_name": "phosphate_rock", "category": "Fertilizer Minerals"},
        {"name": "Potash", "url_name": "potash", "category": "Fertilizer Minerals"},
        {"name": "Sulfur", "url_name": "sulfur", "category": "Industrial Minerals"},
        {"name": "Salt", "url_name": "salt", "category": "Industrial Minerals"},
        {"name": "Fluorspar", "url_name": "fluorspar", "category": "Industrial Minerals"},
        {"name": "Boron", "url_name": "boron", "category": "Industrial Minerals"},
        {"name": "Barite", "url_name": "barite", "category": "Industrial Minerals"},
        {"name": "Bauxite", "url_name": "bauxite", "category": "Industrial Minerals"},
        {"name": "Diamond", "url_name": "diamond", "category": "Industrial Minerals"},
        {"name": "Diatomite", "url_name": "diatomite", "category": "Industrial Minerals"},
        {"name": "Gypsum", "url_name": "gypsum", "category": "Construction Materials"},
        {"name": "Limestone", "url_name": "limestone", "category": "Construction Materials"},
        {"name": "Sand and Gravel", "url_name": "sand_gravel", "category": "Construction Materials"},
        {"name": "Crushed Stone", "url_name": "stone_crushed", "category": "Construction Materials"},
        {"name": "Dimension Stone", "url_name": "stone_dimension", "category": "Construction Materials"},
        {"name": "Clay", "url_name": "clay", "category": "Industrial Minerals"},
        {"name": "Kaolin", "url_name": "kaolin", "category": "Industrial Minerals"},
        {"name": "Bentonite", "url_name": "bentonite", "category": "Industrial Minerals"},
        {"name": "Feldspar", "url_name": "feldspar", "category": "Industrial Minerals"},
        {"name": "Mica", "url_name": "mica", "category": "Industrial Minerals"},
        {"name": "Perlite", "url_name": "perlite", "category": "Industrial Minerals"},
        {"name": "Vermiculite", "url_name": "vermiculite", "category": "Industrial Minerals"},
        {"name": "Talc", "url_name": "talc", "category": "Industrial Minerals"},
        {"name": "Talc", "url_name": "talc", "category": "Industrial Minerals"},
        {"name": "Asbestos", "url_name": "asbestos", "category": "Industrial Minerals"},
        {"name": "Arsenic", "url_name": "arsenic", "category": "Technology Minerals"},
        {"name": "Cadmium", "url_name": "cadmium", "category": "Technology Minerals"},
        {"name": "Mercury", "url_name": "mercury", "category": "Technology Minerals"},
        {"name": "Selenium", "url_name": "selenium", "category": "Technology Minerals"},
        {"name": "Tellurium", "url_name": "tellurium", "category": "Technology Minerals"},
        {"name": "Thallium", "url_name": "thallium", "category": "Technology Minerals"},
        {"name": "Thorium", "url_name": "thorium", "category": "Energy Minerals"},
        {"name": "Helium", "url_name": "helium", "category": "Energy Minerals"},
        {"name": "Bromine", "url_name": "bromine", "category": "Chemical Minerals"},
        {"name": "Iodine", "url_name": "iodine", "category": "Chemical Minerals"},
        {"name": "Sodium Sulfate", "url_name": "sodium-sulfate", "category": "Chemical Minerals"},
        {"name": "Soda Ash", "url_name": "soda_ash", "category": "Chemical Minerals"},
        {"name": "Zeolites", "url_name": "zeolites", "category": "Industrial Minerals"},
        {"name": "Wollastonite", "url_name": "wollastonite", "category": "Industrial Minerals"},
        {"name": "Kyanite", "url_name": "kyanite", "category": "Industrial Minerals"},
        {"name": "Andalusite", "url_name": "kyanite", "category": "Industrial Minerals"},
        {"name": "Sillimanite", "url_name": "kyanite", "category": "Industrial Minerals"},
        {"name": "Garnet", "url_name": "garnet", "category": "Abrasive Minerals"},
        {"name": "Corundum", "url_name": "corundum", "category": "Abrasive Minerals"},
        {"name": "Emery", "url_name": "emery", "category": "Abrasive Minerals"},
        {"name": "Sandpaper", "url_name": "sandpaper", "category": "Abrasive Minerals"},
    ]
    
    print("COMPREHENSIVE USGS DATA COLLECTION")
    print("=" * 50)
    print(f"Collecting data for {len(working_commodities)} commodities...")
    print("Time period: 1996-2025")
    print("")
    
    collector = USGSCollector()
    results = []
    
    # Create results directory (correct path)
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'usgs')
    data_dir = os.path.abspath(data_dir)  # Ensure we have the absolute path
    os.makedirs(data_dir, exist_ok=True)
    
    for i, commodity in enumerate(working_commodities):
        name = commodity["name"]
        url_name = commodity["url_name"]
        category = commodity["category"]
        
        print(f"[{i+1}/{len(working_commodities)}] {name} ({category})...")
        
        try:
            # Collect data from 1996-2025
            data = collector.collect_historical_data(
                commodity=url_name,
                start_year=1996,
                end_year=2025
            )
            
            print(f"  Collected {len(data)} records")
            
            if data:
                # Save to file (using correct path)
                filename = os.path.join(data_dir, f"{url_name}_data_1996_2025.json")
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"  Saved to {filename}")
                
                results.append({
                    "name": name,
                    "url_name": url_name,
                    "category": category,
                    "records": len(data),
                    "file": os.path.join(data_dir, f"{url_name}_data_1996_2025.json")
                })
            else:
                print(f"  No data collected")
                results.append({
                    "name": name,
                    "url_name": url_name,
                    "category": category,
                    "records": 0,
                    "error": "No data collected"
                })
                
        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                "name": name,
                "url_name": url_name,
                "category": category,
                "records": 0,
                "error": str(e)
            })
        
        # Add a small delay to be respectful to the USGS servers
        import time
        time.sleep(0.5)
    
    # Save comprehensive summary
    summary = {
        "total_commodities": len(working_commodities),
        "successful_collections": [r for r in results if r.get("records", 0) > 0],
        "failed_collections": [r for r in results if r.get("records", 0) == 0],
        "total_records": sum(r.get("records", 0) for r in results),
        "by_category": {}
    }
    
    # Group by category
    for result in summary["successful_collections"]:
        category = result["category"]
        if category not in summary["by_category"]:
            summary["by_category"][category] = {
                "commodities": [],
                "total_records": 0
            }
        summary["by_category"][category]["commodities"].append(result["name"])
        summary["by_category"][category]["total_records"] += result["records"]
    
    # Sort categories by total records
    sorted_categories = sorted(
        summary["by_category"].items(), 
        key=lambda x: x[1]["total_records"], 
        reverse=True
    )
    summary["by_category"] = dict(sorted_categories)
    
    summary_file = os.path.join(data_dir, "collection_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print final summary
    successful = len(summary["successful_collections"])
    total_records = summary["total_records"]
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Total commodities attempted: {len(working_commodities)}")
    print(f"Successful collections: {successful}")
    print(f"Failed collections: {len(summary['failed_collections'])}")
    print(f"Success rate: {successful/len(working_commodities)*100:.1f}%")
    print(f"Total records collected: {total_records:,}")
    
    if successful > 0:
        avg_records = total_records / successful
        print(f"Average records per successful commodity: {avg_records:.1f}")
    
    print("\nTop performing categories:")
    for category, data in list(summary["by_category"].items())[:5]:
        print(f"  {category}: {len(data['commodities'])} commodities, {data['total_records']:,} records")
    
    print("\nTop performing commodities:")
    sorted_commodities = sorted(
        summary["successful_collections"], 
        key=lambda x: x["records"], 
        reverse=True
    )
    for commodity in sorted_commodities[:10]:
        print(f"  {commodity['name']}: {commodity['records']:,} records")
    
    if summary["failed_collections"]:
        print(f"\nFailed collections ({len(summary['failed_collections'])}):")
        for result in summary["failed_collections"][:10]:
            print(f"  - {result['name']}: {result.get('error', 'Unknown error')}")
        if len(summary["failed_collections"]) > 10:
            print(f"  ... and {len(summary['failed_collections']) - 10} more")
    
    return summary

def analyze_collected_data():
    """Analyze the collected data to identify patterns and insights"""
    print("\nANALYZING COLLECTED DATA...")
    print("-" * 30)
    
    # Use correct path
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'usgs')
    data_dir = os.path.abspath(data_dir)  # Ensure we have the absolute path
    summary_file = os.path.join(data_dir, "collection_summary.json")
    
    try:
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        # Analyze data quality
        total_records = summary["total_records"]
        successful_count = len(summary["successful_collections"])
        
        if successful_count > 0:
            avg_records = total_records / successful_count
            
            print(f"Overall data quality:")
            print(f"  Total records collected: {total_records:,}")
            print(f"  Average records per commodity: {avg_records:.1f}")
            
            # Find commodities with highest data density
            print(f"\nHigh data density commodities (> {avg_records * 1.5:.0f} records):")
            high_density = [
                c for c in summary["successful_collections"] 
                if c["records"] > avg_records * 1.5
            ]
            for commodity in sorted(high_density, key=lambda x: x["records"], reverse=True)[:5]:
                print(f"  {commodity['name']}: {commodity['records']:,} records")
            
            # Find commodities with low data density
            print(f"\nLow data density commodities (< {avg_records * 0.5:.0f} records):")
            low_density = [
                c for c in summary["successful_collections"] 
                if c["records"] > 0 and c["records"] < avg_records * 0.5
            ]
            for commodity in sorted(low_density, key=lambda x: x["records"])[:5]:
                print(f"  {commodity['name']}: {commodity['records']:,} records")
        
        # Analyze by category completeness
        print(f"\nCategory completeness:")
        for category, data in summary["by_category"].items():
            commodity_count = len(data["commodities"])
            total_records = data["total_records"]
            avg_per_commodity = total_records / commodity_count if commodity_count > 0 else 0
            print(f"  {category}: {commodity_count} commodities, avg {avg_per_commodity:.1f} records/commodity")
        
        print(f"\nAnalysis complete. Data saved to {data_dir}/")
        
    except Exception as e:
        print(f"Error analyzing data: {e}")

if __name__ == "__main__":
    # Collect comprehensive data
    summary = collect_comprehensive_usgs_data()
    
    # Analyze the collected data
    analyze_collected_data()
    
    # Use correct path for final message
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'usgs')
    data_dir = os.path.abspath(data_dir)  # Ensure we have the absolute path
    
    print(f"\n🎉 COMPREHENSIVE DATA COLLECTION COMPLETE!")
    print(f"   Data for {len(summary['successful_collections'])} commodities collected")
    print(f"   Total records: {summary['total_records']:,}")
    print(f"   Results saved to {data_dir}/")