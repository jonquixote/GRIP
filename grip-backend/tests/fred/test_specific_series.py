import requests
import os

def test_specific_series():
    # Test the specific silver series we found
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Test the silver series we found
    series_id = 'A04018GB00LONA286NNBR'
    print(f"Testing silver series: {series_id}")
    
    url = f"{base_url}/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and data['observations']:
                print(f"✓ Success! Found {len(data['observations'])} observations")
                for obs in data['observations']:
                    if obs['value'] != '.':
                        print(f"  Date: {obs['date']}, Price: {obs['value']}")
                        break
            else:
                print("✗ No observations found")
        else:
            print(f"✗ HTTP {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                error_data = response.json()
                print(f"  Error: {error_data}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_specific_series()