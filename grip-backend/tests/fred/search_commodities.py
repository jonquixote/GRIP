import requests
import os

def search_commodities_category():
    # Search the commodities category specifically
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/category'
    
    # Look at category 32217 which is "Commodities"
    category_id = 32217
    
    print(f"Looking at commodities category {category_id}...")
    
    # Get series in this category
    series_url = f"{base_url}/series"
    series_params = {
        'category_id': category_id,
        'api_key': api_key,
        'file_type': 'json',
        'limit': 50
    }
    
    try:
        series_response = requests.get(series_url, params=series_params, timeout=15)
        if series_response.status_code == 200:
            series_data = series_response.json()
            if 'seriess' in series_data and series_data['seriess']:
                print(f"Found {len(series_data['seriess'])} series in commodities category:")
                precious_count = 0
                for series in series_data['seriess']:
                    title = series['title'].lower()
                    # Look for precious metals
                    if ('gold' in title or 'silver' in title or 'platinum' in title or 'palladium' in title) and ('price' in title or 'fixing' in title):
                        precious_count += 1
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
                                    print("    ✗ No data")
                            else:
                                print(f"    ✗ HTTP {test_response.status_code}")
                        except Exception as e:
                            print(f"    ✗ Error testing: {e}")
                        
                        # Limit to 10 precious metal series
                        if precious_count >= 10:
                            break
            else:
                print(f"No series found in commodities category")
        else:
            print(f"Error getting series: HTTP {series_response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_commodities_category()