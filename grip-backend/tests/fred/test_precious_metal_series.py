import requests
import os

def test_precious_metal_series():
    # Test precious metals series with correct API key
    api_key = '95f42f356f5131f13257eac54897e96a'  # Correct key
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Precious metals series IDs to test
    series_ids = [
        'XAUUSD',      # Gold spot price
        'XAGUSD',      # Silver spot price
        'GOLDAMGBD228NLBM',  # LBMA Gold AM Fix
        'GOLDPMGBD228NLBM',  # LBMA Gold PM Fix
        'SLVPRUSD',    # Silver price
    ]
    
    print("Testing precious metals series with correct API key...")
    
    for series_id in series_ids:
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
                    # Find first non-missing value
                    for obs in data['observations']:
                        if obs['value'] != '.':
                            print(f"  ✓ {series_id}: {obs['value']} on {obs['date']}")
                            break
                    else:
                        print(f"  ✗ {series_id}: No valid data")
                else:
                    print(f"  ✗ {series_id}: No observations")
            else:
                print(f"  ✗ {series_id}: HTTP {response.status_code}")
                if response.headers.get('content-type', '').startswith('application/json'):
                    error_data = response.json()
                    if 'error_message' in error_data:
                        print(f"    Error: {error_data['error_message']}")
        except Exception as e:
            print(f"  ✗ {series_id}: Error - {e}")

if __name__ == "__main__":
    test_precious_metal_series()