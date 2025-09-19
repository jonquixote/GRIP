import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import src.main as main_app
from src.models.api_key import APIKey

def set_fred_api_key():
    app = main_app.app
    with app.app_context():
        APIKey.set_key('fred', '95f42f356f5131f13257eac54897e96a')
        print("FRED API key set successfully")

if __name__ == "__main__":
    set_fred_api_key()