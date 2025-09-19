import requests
import os

def search_energy_and_other_commodities():
    # Search for energy and other important commodities
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search terms for important commodities
    search_terms = [
        'crude oil price',
        'natural gas price',
        'coal price',
        'iron ore price',
        'lithium price'
    ]
    
    for term in search_terms:
        print(f"\nSearching for '{term}'...")
        url = base_url
        params = {
            'search_text': term,
            'api_key': api_key,
            'file_type': 'json',
            'limit': 10,
            'order_by': 'popularity',
            'sort_order': 'desc'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'seriess' in data and data['seriess']:
                    for series in data['seriess']:
                        title = series['title'].lower()
                        series_id = series['id']
                        
                        # Check if it's a price series
                        if 'price' in title:
                            print(f"  - {series_id}: {series['title']} (Frequency: {series.get('frequency', 'Unknown')})")
                            
                            # Test this series
                            test_url = f"https://api.stlouisfed.org/fred/series/observations"
                            test_params = {
                                'series_id': series_id,
                                'api_key': api_key,
                                'file_type': 'json',
                                'limit': 3,
                                'sort_order': 'desc'
                            }
                            
                            try:
                                test_response = requests.get(test_url, params=test_params, timeout=10)
                                if test_response.status_code == 200:
                                    test_data = test_response.json()
                                    if 'observations' in test_data and test_data['observations']:
                                        # Find first non-missing value
                                        for obs in test_data['observations']:
                                            if obs['value'] != '.':
                                                print(f"    ✓ Works! Latest value: {obs['value']} on {obs['date']}")
                                                break
                                else:
                                    print(f"    ✗ HTTP {test_response.status_code}")
                            except Exception as e:
                                print(f"    ✗ Error testing: {e}")
                else:
                    print("No series found")
            else:
                print(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    search_energy_and_other_commodities()