import requests
import os

def search_global_precious_metals():
    # Search specifically for the global metal price pattern
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search for all series that follow the global metal price pattern
    print("Searching for global metal price series (PXXXXUSDM pattern)...")
    url = base_url
    params = {
        'search_text': 'P*USDM',
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
                print(f"Found {len(data['seriess'])} series matching pattern:")
                precious_count = 0
                for series in data['seriess']:
                    title = series['title'].lower()
                    series_id = series['id']
                    
                    # Check if it's a precious metal
                    if 'gold' in title or 'silver' in title or 'platinum' in title or 'palladium' in title:
                        precious_count += 1
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
                        
                        # Limit to 10 precious metals
                        if precious_count >= 10:
                            break
            else:
                print("No series found")
        else:
            print(f"HTTP {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_global_precious_metals()