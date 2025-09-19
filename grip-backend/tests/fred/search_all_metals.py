import requests
import os

def search_all_metal_prices():
    # Search for all metal price series
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    print("Searching for all metal price series...")
    url = base_url
    params = {
        'search_text': 'metal price',
        'api_key': api_key,
        'file_type': 'json',
        'limit': 100,
        'order_by': 'popularity',
        'sort_order': 'desc'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'seriess' in data and data['seriess']:
                print(f"Found {len(data['seriess'])} metal price series:")
                precious_metals = []
                base_metals = []
                
                for series in data['seriess']:
                    title = series['title'].lower()
                    series_id = series['id']
                    
                    # Categorize metals
                    if 'gold' in title or 'silver' in title or 'platinum' in title or 'palladium' in title:
                        if series_id not in [s['id'] for s in precious_metals]:
                            precious_metals.append(series)
                    elif 'copper' in title or 'aluminum' in title or 'nickel' in title or 'zinc' in title or 'lead' in title or 'tin' in title:
                        if series_id not in [s['id'] for s in base_metals]:
                            base_metals.append(series)
                
                print(f"\nPrecious Metals ({len(precious_metals)} series):")
                for series in precious_metals[:10]:  # Show top 10
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
                
                print(f"\nBase Metals ({len(base_metals)} series):")
                for series in base_metals[:10]:  # Show top 10
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
    search_all_metal_prices()