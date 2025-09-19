import requests
import os

def test_precious_metal_series_ids():
    # Test potential series IDs for gold and silver
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Potential series IDs for precious metals following the pattern we saw
    potential_series = [
        'PGOLDUSDM',    # Hypothetical gold series
        'PSILVUSDM',    # Hypothetical silver series
        'PPLATUSDM',    # Platinum
        'PPALLUSDM',    # Palladium
        'PGOLDUSDQ',    # Quarterly gold
        'PSILVUSDQ',    # Quarterly silver
    ]
    
    print("Testing potential precious metal series IDs...")
    
    for series_id in potential_series:
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
                        'limit': 1,
                        'sort_order': 'desc'
                    }
                    
                    obs_response = requests.get(obs_url, params=obs_params, timeout=10)
                    if obs_response.status_code == 200:
                        obs_data = obs_response.json()
                        if 'observations' in obs_data and obs_data['observations']:
                            for obs in obs_data['observations']:
                                if obs['value'] != '.':
                                    print(f"    Latest value: {obs['value']} on {obs['date']}")
                                    break
                    else:
                        print(f"    Error getting observations: HTTP {obs_response.status_code}")
                else:
                    print(f"  ? {series_id}: No series info (might not exist)")
            else:
                print(f"  ? {series_id}: HTTP {response.status_code} (might not exist)")
        except Exception as e:
            print(f"  ? {series_id}: Error - {e}")

if __name__ == "__main__":
    test_precious_metal_series_ids()