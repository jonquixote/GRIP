import requests
import os

def browse_fred_categories():
    # Browse FRED categories to find precious metals
    api_key = '95f42f356f5131f13257eac54897e96a'
    base_url = 'https://api.stlouisfed.org/fred/category'
    
    # Start with the root category and drill down
    categories_to_check = [0]  # Root category
    
    while categories_to_check:
        category_id = categories_to_check.pop(0)
        
        # Get children of this category
        url = f"{base_url}/children"
        params = {
            'category_id': category_id,
            'api_key': api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'categories' in data and data['categories']:
                    print(f"Category {category_id} has {len(data['categories'])} children:")
                    for category in data['categories']:
                        print(f"  - {category['id']}: {category['name']}")
                        
                        # Check if this category might contain precious metals
                        name = category['name'].lower()
                        if 'precious' in name or 'metal' in name or 'gold' in name or 'silver' in name:
                            print(f"    *** POTENTIAL MATCH ***")
                            
                            # Get series in this category
                            series_url = f"{base_url}/series"
                            series_params = {
                                'category_id': category['id'],
                                'api_key': api_key,
                                'file_type': 'json',
                                'limit': 10
                            }
                            
                            try:
                                series_response = requests.get(series_url, params=series_params, timeout=15)
                                if series_response.status_code == 200:
                                    series_data = series_response.json()
                                    if 'seriess' in series_data and series_data['seriess']:
                                        print(f"    Series in this category:")
                                        for series in series_data['seriess']:
                                            title = series['title'].lower()
                                            if 'price' in title or 'fixing' in title:
                                                print(f"      - {series['id']}: {series['title']}")
                                    else:
                                        print(f"    No series found in this category")
                                else:
                                    print(f"    Error getting series: HTTP {series_response.status_code}")
                            except Exception as e:
                                print(f"    Error getting series: {e}")
                        
                        # Add to check list if not too deep
                        if len(categories_to_check) < 20:
                            categories_to_check.append(category['id'])
                else:
                    print(f"Category {category_id} has no children")
            else:
                print(f"Error getting children of category {category_id}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error with category {category_id}: {e}")
        
        # Limit the number of categories we check
        if len(categories_to_check) > 50:
            break

if __name__ == "__main__":
    browse_fred_categories()