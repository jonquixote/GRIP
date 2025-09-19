import requests
import os

def search_fixing_series():
    # Search for fixing price series
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search for fixing series
    search_terms = ['fixing price', 'spot price']
    
    for term in search_terms:
        print(f"\nSearching for '{term}' series...")
        url = base_url
        params = {
            'search_text': term,
            'api_key': api_key,
            'file_type': 'json',
            'limit': 20,
            'order_by': 'popularity',
            'sort_order': 'desc'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'seriess' in data and data['seriess']:
                    print(f"Found {len(data['seriess'])} series:")
                    for series in data['seriess']:
                        title = series['title'].lower()
                        # Look for metal fixing prices
                        if 'gold' in title or 'silver' in title or 'metal' in title:
                            print(f"  - {series['id']}: {series['title']}")
                            
                            # Test this series
                            test_url = f"https://api.stlouisfed.org/fred/series/observations"
                            test_params = {
                                'series_id': series['id'],
                                'api_key': api_key,
                                'file_type': 'json',
                                'limit': 3
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
                                            print("    ✗ No valid data")
                                    else:
                                        print("    ✗ No data")
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
    search_fixing_series()