import requests
import os

def search_global_metal_prices():
    # Search for global metal price series with the pattern we saw
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search for global metal prices
    print("Searching for global metal price series...")
    url = base_url
    params = {
        'search_text': 'Global price',
        'api_key': api_key,
        'file_type': 'json',
        'limit': 50,
        'order_by': 'popularity',
        'sort_order': 'desc'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'seriess' in data and data['seriess']:
                print(f"Found {len(data['seriess'])} global price series:")
                metals_found = []
                for series in data['seriess']:
                    title = series['title'].lower()
                    # Look for metal prices
                    if 'price' in title and 'global' in title and ('metal' in title or 'copper' in title or 'aluminum' in title or 'nickel' in title or 'zinc' in title or 'lead' in title or 'tin' in title or 'gold' in title or 'silver' in title):
                        # Check if we already have this metal
                        metal_name = None
                        for metal in ['copper', 'aluminum', 'nickel', 'zinc', 'lead', 'tin', 'gold', 'silver']:
                            if metal in title:
                                metal_name = metal
                                break
                        
                        if metal_name and metal_name not in metals_found:
                            metals_found.append(metal_name)
                            print(f"  - {series['id']}: {series['title']} (Frequency: {series.get('frequency', 'Unknown')})")
                            
                            # Test this series
                            test_url = f"https://api.stlouisfed.org/fred/series/observations"
                            test_params = {
                                'series_id': series['id'],
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
    search_global_metal_prices()