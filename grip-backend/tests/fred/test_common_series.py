import requests
import os

def test_common_series_ids():
    # Test common precious metals series IDs
    api_key = '95f42f356f5131f23257eac54897e96a'  # Intentionally wrong key to test
    base_url = 'https://api.stlouisfed.org/fred'
    
    # Common precious metals series IDs
    series_ids = [
        'XAUUSD',      # Gold spot price (common in financial data)
        'XAGUSD',      # Silver spot price (common in financial data)
        'GOLDAMGBD228NLBM',  # LBMA Gold AM Fix
        'GOLDPMGBD228NLBM',  # LBMA Gold PM Fix
        'SLVPRUSD',    # Silver price
        'DCOILBRENTECO',  # Brent crude (to verify API key works)
    ]
    
    print("Testing common precious metals series IDs...")
    print("(Note: Using intentionally wrong API key to test if series exist)")
    
    for series_id in series_ids:
        url = f"{base_url}/series"
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            # Even with a wrong API key, if the series exists, we should get a 400 with a specific error
            if response.status_code == 400:
                error_data = response.json()
                if 'error_message' in error_data and 'api_key' in error_data['error_message'].lower():
                    print(f"  ? {series_id}: Series might exist (API key error)")
                elif 'error_message' in error_data and 'series' in error_data['error_message'].lower():
                    print(f"  ✗ {series_id}: Series does not exist")
                else:
                    print(f"  ? {series_id}: Unknown error - {error_data}")
            elif response.status_code == 200:
                print(f"  ✓ {series_id}: Series exists and accessible")
            else:
                print(f"  ? {series_id}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ? {series_id}: Error - {e}")

if __name__ == "__main__":
    test_common_series_ids()