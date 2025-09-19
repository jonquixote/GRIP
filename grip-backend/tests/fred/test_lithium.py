import requests
import os

def test_lithium_series():
    # Test if lithium series exists
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    series_id = 'PLITHUSDM'
    print(f"Testing lithium series: {series_id}")
    
    url = f"{base_url}/series"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'seriess' in data and data['seriess']:
                series_info = data['seriess'][0]
                print(f"  ✓ {series_id}: {series_info['title']}")
                
                # Get a recent observation
                obs_url = f"{base_url}/series/observations"
                obs_params = {
                    'series_id': series_id,
                    'api_key': api_key,
                    'file_type': 'json',
                    'limit': 3,
                    'sort_order': 'desc'
                }
                
                obs_response = requests.get(obs_url, params=obs_params, timeout=10)
                if obs_response.status_code == 200:
                    obs_data = obs_response.json()
                    if 'observations' in obs_data and obs_data['observations']:
                        print(f"  Recent values:")
                        for obs in obs_data['observations']:
                            if obs['value'] != '.':
                                print(f"    {obs['date']}: {obs['value']}")
                else:
                    print(f"  Error getting observations: HTTP {obs_response.status_code}")
            else:
                print(f"  ? {series_id}: No series info")
        else:
            print(f"  ? {series_id}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  ? {series_id}: Error - {e}")

if __name__ == "__main__":
    test_lithium_series()