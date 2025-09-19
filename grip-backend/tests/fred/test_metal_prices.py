import requests
import os

def test_metal_price_series():
    # Test the metal price series we found
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Metal price series IDs
    series_ids = [
        'PCOPPUSDM',  # Global price of Copper
        'PALUMUSDM',  # Global price of Aluminum
        'PCOPPUSDQ',  # Global price of Copper (Quarterly)
    ]
    
    print("Testing metal price series...")
    
    for series_id in series_ids:
        print(f"\n{series_id}:")
        
        # Get series info
        url = f"{base_url}/series"
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'seriess' in data and data['seriess']:
                    series_info = data['seriess'][0]
                    print(f"  Title: {series_info['title']}")
                    print(f"  Units: {series_info['units']}")
                    print(f"  Frequency: {series_info['frequency']}")
                    print(f"  Seasonal Adjustment: {series_info['seasonal_adjustment']}")
                    
                    # Get recent observations
                    obs_url = f"{base_url}/series/observations"
                    obs_params = {
                        'series_id': series_id,
                        'api_key': api_key,
                        'file_type': 'json',
                        'limit': 5,
                        'sort_order': 'desc'
                    }
                    
                    obs_response = requests.get(obs_url, params=obs_params, timeout=15)
                    if obs_response.status_code == 200:
                        obs_data = obs_response.json()
                        if 'observations' in obs_data and obs_data['observations']:
                            print(f"  Recent values:")
                            for obs in obs_data['observations']:
                                if obs['value'] != '.':
                                    print(f"    {obs['date']}: {obs['value']}")
                        else:
                            print("  No observations found")
                    else:
                        print(f"  Error getting observations: HTTP {obs_response.status_code}")
                else:
                    print("  No series info returned")
            else:
                print(f"  Error getting series info: HTTP {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_metal_price_series()