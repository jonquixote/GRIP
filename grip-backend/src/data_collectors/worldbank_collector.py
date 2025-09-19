import requests
import os
from typing import Dict, List, Any, Optional
import datetime
from .base_collector import BaseDataCollector

class WorldBankCollector(BaseDataCollector):
    """Data collector for World Bank data"""

    def __init__(self):
        super().__init__(
            name="WorldBank",
            base_url="https://api.worldbank.org/v2"
        )
        
        # Mining and mineral related indicators
        self.mineral_indicators = {
            'mining_gdp': 'NV.IND.MINQ.ZS',  # Mining, value added (% of GDP)
            'mineral_exports': 'TX.VAL.MMTL.ZS.UN',  # Ores and metals exports (% of merchandise exports)
            'fuel_exports': 'TX.VAL.FUEL.ZS.UN',  # Fuel exports (% of merchandise exports)
            'natural_resources_rents': 'NY.GDP.TOTL.RT.ZS',  # Total natural resources rents (% of GDP)
            'mineral_rents': 'NY.GDP.MINR.RT.ZS',  # Mineral rents (% of GDP)
        }
        
        self.min_request_interval = 0.5  # Be respectful to World Bank API

    def _get_indicator_detail(self, indicator_code: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an indicator from World Bank API"""
        try:
            url = f"{self.base_url}/source/2/series/{indicator_code}?format=json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 1:
                return data
            return None
        except Exception as e:
            self.logger.error(f"Error getting indicator detail for {indicator_code}: {e}")
            return None

    def _collect_indicator_data(self, indicator_code: str, indicator_name: str,
                               countries: List[str],
                               years: List[int]) -> List[Dict[str, Any]]:
        """Internal method that requires non-empty lists for countries and years"""
        try:
            country_list = countries if 'all' not in countries else []
            
            url = f"{self.base_url}/countries/{','.join(country_list) or 'all'}/indicators/{indicator_code}"
            params = {
                'date': f"{min(years)}:{max(years)}",
                'format': 'json',
                'per_page': 1000
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if data and len(data) > 1:
                for entry in data:
                    country_id = entry.get('country', {}).get('id') 
                    if not country_id and 'countryiso3code' in entry:
                        country_id = entry['countryiso3code']
                    
                    country_name = entry.get('country', {}).get('value')
                    if not country_name and 'country' in entry:
                        country_name = entry['country']
                    
                    results.append({
                        'indicator_code': indicator_code,
                        'indicator_name': indicator_name,
                        'country_code': country_id,
                        'country_name': country_name,
                        'value': entry.get('value'),
                        'year': entry.get('date'),
                        'source': 'WorldBank',
                        'collected_at': datetime.datetime.utcnow().isoformat()
                    })
            return results
        except Exception as e:
            self.logger.error(f"Error collecting indicator data for {indicator_code}: {e}")
            return []

    def collect_data(self, indicator: Optional[str] = None, 
                    countries: Optional[List[str]] = None, 
                    years: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """Collect World Bank indicator data"""
        
        results = []
        if indicator:
            indicator_name = indicator
            if indicator in self.mineral_indicators:
                indicator_code = self.mineral_indicators[indicator]
            else:
                detail = self._get_indicator_detail(indicator)
                if detail:
                    indicator_code = indicator
                    indicator_name = detail.get('name', indicator)
                else:
                    self.logger.error(f"Invalid indicator code: {indicator}")
                    return results
            
            safe_countries = ['all'] if countries is None else countries
            safe_years = [datetime.datetime.now().year - 1] if years is None else years
            data = self._collect_indicator_data(indicator_code, indicator_name, safe_countries, safe_years)
            results.extend(data)
        
        else:
            safe_countries = ['all'] if countries is None else countries
            safe_years = [datetime.datetime.now().year - 1] if years is None else years
            for ind, indicator_code in self.mineral_indicators.items():
                data = self._collect_indicator_data(indicator_code, ind, safe_countries, safe_years)
                results.extend(data)
        
        return results

    def get_country_data(self, country_code: str, 
                        countries: Optional[List[str]] = None, 
                        years: Optional[List[int]] = None) -> Dict[str, Any]:
        """Get country-specific data from World Bank API"""
        try:
            url = f"{self.base_url}/countries/{country_code}?format=json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return {
                'country_code': country_code,
                'name': data['name'],
                'region': data['region']['value'],
                'income_level': data['incomeLevel']['value'],
                'capital_city': data['capitalCity'],
                'longitude': data['longitude'],
                'latitude': data['latitude']
            } if data and len(data) > 1 else {}
        except Exception as e:
            self.logger.error(f"Error getting country data for {country_code}: {e}")
            return {}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate a single data point"""
        required_fields = ['indicator_code', 'country_code', 'year', 'source']
        
        for field in required_fields:
            if field not in data:
                return False
        
        try:
            year = int(data['year'])
            if year < 1960 or year > datetime.datetime.now().year:
                return False
        except (ValueError, TypeError):
            return False
        
        if len(data.get('country_code', '')) != 3:
            return False
        
        return True

    def get_available_indicators(self) -> Dict[str, str]:
        """Get available mineral-related indicators"""
        return self.mineral_indicators.copy()

    def search_indicators(self, query: str, page_size: int = 10) -> List[Dict[str, Any]]:
        """Search for indicators by keyword"""
        try:
            url = f"{self.base_url}/source/2/series"
            params = {
                'format': 'json',
                'q': query,
                'per_page': page_size
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if data and len(data) > 1:
                for item in data:
                    results.append({
                        'id': item['id'],
                        'value': item['value'],
                        'source': item['sourceOrganization']
                    })
            return results
        except Exception as e:
            self.logger.error(f"Error searching indicators: {e}")
            return []
