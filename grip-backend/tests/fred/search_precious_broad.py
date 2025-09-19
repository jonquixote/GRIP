import requests
import os

def search_precious_metals_broad():
    # Search for precious metals more broadly
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Search terms for precious metals
    search_terms = [
        'precious metal',
        'noble metal',
        'platinum group',
        'platinum price',
        'palladium price'
    ]
    
    for term in search_terms:
        print("\nSearching for '" + term + "'...")
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
                    precious_count = 0
                    for series in data['seriess']:
                        title = series['title'].lower()
                        # Look for metal prices
                        if 'price' in title and ('gold' in title or 'silver' in title or 'platinum' in title or 'palladium' in title):
                            precious_count += 1
                            print("  - " + series['id'] + ": " + series['title'] + " (Frequency: " + str(series.get('frequency', 'Unknown')) + ")")
                            
                            # Test this series
                            test_url = "https://api.stlouisfed.org/fred/series/observations"
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
                                                print("    ✓ Works! Latest value: " + str(obs['value']) + " on " + str(obs['date']))
                                                break
                                else:
                                    print("    ✗ HTTP " + str(test_response.status_code))
                            except Exception as e:
                                print("    ✗ Error testing: " + str(e))
                            
                            # Limit to 3 series
                            if precious_count >= 3:
                                break
                else:
                    print("No series found")
            else:
                print("HTTP " + str(response.status_code))
        except Exception as e:
            print("Error: " + str(e))

if __name__ == "__main__":
    search_precious_metals_broad()