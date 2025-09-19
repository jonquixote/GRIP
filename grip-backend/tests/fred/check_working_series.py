import requests
import os

def check_working_series():
    # Check the working silver series we found earlier
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    # The silver series that worked
    series_id = 'A04018GB00LONA286NNBR'
    print(f"Checking working silver series: {series_id}")
    
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
                print(f"Title: {series_info['title']}")
                print(f"Frequency: {series_info['frequency']}")
                print(f"Units: {series_info['units']}")
                print(f"Seasonal Adjustment: {series_info['seasonal_adjustment']}")
                print(f"Last Updated: {series_info['last_updated']}")
                
                # Get observations
                obs_url = f"{base_url}/series/observations"
                obs_params = {
                    'series_id': series_id,
                    'api_key': api_key,
                    'file_type': 'json',
                    'limit': 10
                }
                
                obs_response = requests.get(obs_url, params=obs_params, timeout=15)
                if obs_response.status_code == 200:
                    obs_data = obs_response.json()
                    if 'observations' in obs_data and obs_data['observations']:
                        print(f"\nRecent observations:")
                        for obs in obs_data['observations'][:5]:
                            if obs['value'] != '.':
                                print(f"  {obs['date']}: {obs['value']}")
                else:
                    print(f"Error getting observations: HTTP {obs_response.status_code}")
            else:
                print("No series info returned")
        else:
            print(f"Error getting series info: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_working_series()