import requests
import os

def search_precious_metal_prices():
    # Search for precious metal price series
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search for gold and silver specifically
    metals = ['gold', 'silver']
    
    for metal in metals:
        print(f"\nSearching for Global price of {metal}...")
        url = base_url
        params = {
            'search_text': f'Global price of {metal}',
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
                        if metal in title:
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
    search_precious_metal_prices()