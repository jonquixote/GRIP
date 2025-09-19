import requests
import os

def find_similar_metal_series():
    # Find series similar to the working metal series
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/series/search'
    
    # Working metal series we've found
    working_series = [
        'PCOPPUSDM',  # Copper
        'PALUMUSDM',  # Aluminum
        'PNICKUSDM',  # Nickel
        'PZINCUSDM',  # Zinc
        'PLEADUSDM',  # Lead
    ]
    
    # Try to find the pattern by looking at similar series
    print("Looking for series similar to working metal series...")
    
    for base_series in working_series:
        print(f"\nSearching for series similar to {base_series}...")
        # Try different metal abbreviations
        metals = ['GOLD', 'SILV', 'PLAT', 'PALL', 'TIN']
        
        for metal in metals:
            # Try different patterns
            patterns = [
                f'P{metal}USDM',
                f'P{metal}USDQ',
                f'P{metal}USDY',
            ]
            
            for pattern in patterns:
                url = f"{base_url}/series"
                params = {
                    'series_id': pattern,
                    'api_key': api_key,
                    'file_type': 'json'
                }
                
                try:
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if 'seriess' in data and data['seriess']:
                            series_info = data['seriess'][0]
                            print(f"  ✓ {pattern}: {series_info['title']}")
                            
                            # Get a recent observation
                            obs_url = f"https://api.stlouisfed.org/fred/series/observations"
                            obs_params = {
                                'series_id': pattern,
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
                    elif response.status_code != 400:
                        print(f"  ? {pattern}: HTTP {response.status_code}")
                except Exception as e:
                    pass  # Ignore errors for non-existent series

if __name__ == "__main__":
    find_similar_metal_series()