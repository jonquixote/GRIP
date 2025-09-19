import requests
import os

def search_alternative_precious_metals():
    # Search for alternative precious metal series
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Alternative search terms for precious metals
    search_terms = [
        'LBMA',
        'London Bullion',
        ' precious ',
        'noble metal price',
        'metal fixing'
    ]
    
    for term in search_terms:
        print(f"\nSearching for '{term.strip()}'...")
        url = base_url
        params = {
            'search_text': term.strip(),
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
                    precious_count = 0
                    for series in data['seriess']:
                        title = series['title'].lower()
                        series_id = series['id']
                        
                        # Look for precious metals
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
                            
                            # Limit to 5 series
                            if precious_count >= 5:
                                break
                else:
                    print("No series found")
            else:
                print(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    search_alternative_precious_metals()