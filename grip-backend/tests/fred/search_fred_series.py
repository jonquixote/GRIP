import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import src.main as main_app
from src.data_collectors.fred_collector import FREDCollector

def search_for_precious_metal_prices():
    app = main_app.app
    with app.app_context():
        collector = FREDCollector()
        
        # Search for more specific gold price series
        print("Searching for gold price series...")
        gold_result = collector.search_commodity_series("gold price")
        if gold_result['success']:
            print(f"Found {gold_result['filtered_count']} gold price series:")
            for series in gold_result['series'][:10]:  # Show first 10
                print(f"  - {series['id']}: {series['title']}")
        else:
            print(f"Error searching for gold price: {gold_result['error']}")
        
        print("\nSearching for silver price series...")
        silver_result = collector.search_commodity_series("silver price")
        if silver_result['success']:
            print(f"Found {silver_result['filtered_count']} silver price series:")
            for series in silver_result['series'][:10]:  # Show first 10
                print(f"  - {series['id']}: {series['title']}")
        else:
            print(f"Error searching for silver price: {silver_result['error']}")

if __name__ == "__main__":
    search_for_precious_metal_prices()