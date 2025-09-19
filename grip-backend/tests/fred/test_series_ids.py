import requests
import os

def test_series_ids():
    # Test some common gold and silver series IDs
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Common gold and silver series IDs
    series_ids = [
        'GOLDAMGBD228NLBM',  # Gold fixing price
        'GOLDPMGBD228NLBM',  # Gold fixing price (PM)
        'XAUUSD',            # Gold price (might not exist)
        'SILVER',            # Silver price (might not exist)
        'SLVPRUSD',          # Silver price
        'XAGUSD',            # Silver price (might not exist)
    ]
    
    for series_id in series_ids:
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
                    print(f"✓ {series_id}: {data['seriess'][0]['title']}")
                else:
                    print(f"✗ {series_id}: No data returned")
            else:
                print(f"✗ {series_id}: HTTP {response.status_code}")
        except Exception as e:
            print(f"✗ {series_id}: Error - {e}")

if __name__ == "__main__":
    test_series_ids()