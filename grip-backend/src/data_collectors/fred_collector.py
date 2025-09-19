import requests
import pandas as pd
import json
import os
import logging
from datetime import datetime, timedelta
from .base_collector import BaseDataCollector
from src.models.api_key import APIKey

class FREDCollector(BaseDataCollector):
    def __init__(self):
        super().__init__(name="FRED", base_url="https://api.stlouisfed.org/fred")
        # Try to get API key from environment variable first, then from database
        self.api_key = os.getenv('FRED_API_KEY') or APIKey.get_key('fred')
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'fred')
        
        # Set up logging
        self.logger = logging.getLogger(f"collector.{self.name}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        # Rate limiting - FRED allows 120 requests per minute
        self.min_request_interval = 0.5  # 2 requests per second to be safe
        
        # FRED commodity series mapping
        # Base metals that we've confirmed are available on FRED
        self.commodity_series = {
            # Base metals
            'copper': 'PCOPPUSDM',        # Global price of Copper, U.S. Dollars per Metric Ton
            'aluminum': 'PALUMUSDM',      # Global price of Aluminum, U.S. Dollars per Metric Ton
            'nickel': 'PNICKUSDM',        # Global price of Nickel, U.S. Dollars per Metric Ton
            'zinc': 'PZINCUSDM',          # Global price of Zinc, U.S. Dollars per Metric Ton
            'lead': 'PLEADUSDM',          # Global price of Lead, U.S. Dollars per Metric Ton
            'tin': 'PTINUSDQ',            # Global price of Tin, U.S. Dollars per Metric Ton (quarterly)
            # Energy commodities
            'oil_wti': 'DCOILWTICO',      # Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma
            'oil_brent': 'DCOILBRENTEU',  # Crude Oil Prices: Brent - Europe
            'natural_gas': 'DHHNGSP',     # Henry Hub Natural Gas Spot Price
            'coal': 'PCOALAUUSDM',        # Global price of Coal, Australian thermal coal
            'uranium': 'PURANUSDM',       # Global price of Uranium, U.S. Dollars per Pound
            'propane': 'DPROPANEMBTX',    # Propane Prices: Mont Belvieu, Texas, U.S. Dollars per Gallon
            'heating_oil': 'DHOILNYH',    # No. 2 Heating Oil Prices: New York Harbor, U.S. Dollars per Gallon
            'diesel': 'GASDESW',          # US Diesel Sales Price, U.S. Dollars per Gallon
            'gasoline': 'GASREGW',        # US Regular All Formulations Gas Price, U.S. Dollars per Gallon
            # Agricultural commodities
            'wheat': 'PWHEAMTUSDM',       # Global price of Wheat, U.S. Dollars per Metric Ton
            'corn': 'PMAIZMTUSDM',        # Global price of Corn, U.S. Dollars per Metric Ton
            'soybeans': 'PSOYBUSDM',      # Global price of Soybeans, U.S. Dollars per Metric Ton
            'rice': 'PRICENPQUSDM',        # Global price of Rice, U.S. Dollars per Metric Ton
            'cotton': 'PCOTTINDUSDM',     # Global price of Cotton, U.S. Cents per Pound
            'sugar': 'PSUGAISAUSDM',      # Global price of Sugar, No. 11, World, U.S. Cents per Pound
            'coffee': 'PCOFFOTMUSDM',     # Global price of Coffee, Other Mild Arabica, U.S. Dollars per Metric Ton
            'cocoa': 'PCOCOUSDM',          # Global price of Cocoa, U.S. Dollars per Metric Ton
            'palm_oil': 'PPOILUSDM',      # Global price of Palm Oil, U.S. Dollars per Metric Ton
            # Other commodities
            'iron_ore': 'PIORECRUSDM',    # Global price of Iron Ore
        }
        
        # Create organized data directory structure
        self._create_data_directories()
        
    def _create_data_directories(self):
        """Create organized directory structure for FRED data"""
        # Main data directory
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Subdirectories for different data types
        self.commodities_dir = os.path.join(self.data_dir, 'commodities')
        self.economic_indicators_dir = os.path.join(self.data_dir, 'economic_indicators')
        self.metadata_dir = os.path.join(self.data_dir, 'metadata')
        self.search_results_dir = os.path.join(self.data_dir, 'search_results')
        
        # Create all subdirectories
        for directory in [self.commodities_dir, self.economic_indicators_dir, 
                         self.metadata_dir, self.search_results_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create commodity-specific directories
        for commodity in self.commodity_series.keys():
            commodity_dir = os.path.join(self.commodities_dir, commodity)
            os.makedirs(commodity_dir, exist_ok=True)
        
    def test_connection(self):
        """Test FRED API connection"""
        if not self.api_key:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            # Test with a simple series request
            url = f"{self.base_url}/series"
            params = {
                'series_id': 'GDPC1',  # Real GDP series
                'api_key': self.api_key,
                'file_type': 'json'
            }
            
            self.logger.info("Testing FRED API connection")
            response = self._make_request(url, params=params)
            
            if response and 'seriess' in response and response['seriess']:
                success_msg = 'FRED API connection successful'
                self.logger.info(success_msg)
                return {
                    'success': True, 
                    'message': success_msg,
                    'test_series': response['seriess'][0]['title'],
                    'api_key_valid': True
                }
            else:
                error_msg = 'Unexpected API response format or empty response'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
        except requests.exceptions.Timeout:
            error_msg = 'FRED API connection timeout'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f'FRED API connection error: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f'Unexpected error testing FRED API connection: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def collect_price_data(self, commodity_name, start_date=None, end_date=None, limit=1000):
        """Collect price data for a commodity from FRED"""
        if not self.api_key:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # Find the series ID for this commodity
        series_id = None
        commodity_lower = commodity_name.lower()
        
        # Direct match
        if commodity_lower in self.commodity_series:
            series_id = self.commodity_series[commodity_lower]
        else:
            # Try partial matches
            for key, value in self.commodity_series.items():
                if commodity_lower in key or key in commodity_lower:
                    series_id = value
                    break
        
        if not series_id:
            error_msg = f'No FRED series found for commodity: {commodity_name}. Available: {list(self.commodity_series.keys())}'
            self.logger.error(error_msg)
            return {
                'success': False, 
                'error': error_msg
            }
        
        try:
            # Get the actual data
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc'
            }
            
            if start_date:
                params['observation_start'] = start_date
            if end_date:
                params['observation_end'] = end_date
            
            self.logger.info(f"Making request to FRED API for {commodity_name} ({series_id})")
            response = self._make_request(url, params=params)
            
            if response:
                observations = response.get('observations', [])
                
                # Process the data
                price_data = []
                for obs in observations:
                    if obs['value'] != '.':  # FRED uses '.' for missing values
                        try:
                            data_point = {
                                'date': obs['date'],
                                'price': float(obs['value']),
                                'commodity': commodity_name,
                                'source': 'FRED',
                                'series_id': series_id,
                                'realtime_start': obs.get('realtime_start'),
                                'realtime_end': obs.get('realtime_end')
                            }
                            
                            # Validate data point
                            if self.validate_data(data_point):
                                price_data.append(data_point)
                            else:
                                self.logger.warning(f"Invalid data point for {commodity_name}: {data_point}")
                        except (ValueError, TypeError) as e:
                            self.logger.warning(f"Error processing observation for {commodity_name}: {e}")
                            continue
                
                # Get series metadata
                series_info = self.get_series_info(series_id)
                
                # Save series metadata
                if series_info:
                    metadata_filename = f"{commodity_name}_metadata.json"
                    self.save_data_to_file(series_info, metadata_filename, data_type='metadata')
                
                self.logger.info(f"Successfully collected {len(price_data)} valid records for {commodity_name}")
                return {
                    'success': True,
                    'data': price_data,
                    'series_id': series_id,
                    'count': len(price_data),
                    'commodity': commodity_name,
                    'series_info': series_info
                }
            else:
                error_msg = f'Failed to get response from FRED API for {commodity_name}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = f'Request timeout for {commodity_name}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f'Request error for {commodity_name}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f'Unexpected error collecting data for {commodity_name}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_series_info(self, series_id):
        """Get metadata about a FRED series"""
        if not self.api_key:
            self.logger.warning("No API key available for series info request")
            return None
        
        try:
            url = f"{self.base_url}/series"
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json'
            }
            
            self.logger.info(f"Fetching series info for {series_id}")
            response = self._make_request(url, params=params)
            
            if response and 'seriess' in response and response['seriess']:
                return response['seriess'][0]
            else:
                self.logger.warning(f"Unexpected response format for series info: {series_id}")
                return None
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout getting series info for {series_id}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error getting series info for {series_id}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error getting series info for {series_id}: {e}")
            return None
    
    def collect_data(self, commodity_id=None, data_type='price'):
        """Collect data from FRED. If commodity_id is None, collect for all commodities."""
        if commodity_id is None:
            # Collect data for all commodities
            return self.collect_all_commodities_data()
        else:
            # Legacy method for compatibility with base collector
            # Get commodity name from database
            try:
                from src.models.commodity import Commodity
                commodity = Commodity.query.get(commodity_id)
                if not commodity:
                    return {'success': False, 'error': f'Commodity with ID {commodity_id} not found'}
                
                result = self.collect_price_data(commodity.name.lower())
                if result['success']:
                    # Save data to file in organized structure
                    filename = f"{commodity.name.lower()}_data.json"
                    self.save_data_to_file(result, filename, data_type='commodity', commodity_name=commodity.name.lower())
                    
                    return {
                        'success': True,
                        'data': result['data'],
                        'source': 'FRED',
                        'commodity_id': commodity_id
                    }
                else:
                    return result
                    
            except Exception as e:
                return {'success': False, 'error': str(e)}


    def validate_data(self, data):
        """Validate a single data point"""
        required_fields = ['date', 'price', 'commodity', 'source']
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                self.logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate price is positive
        try:
            price = float(data['price'])
            if price <= 0:
                self.logger.warning(f"Invalid price value: {price}")
                return False
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid price type: {data['price']}")
            return False
        
        # Validate date format
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            self.logger.warning(f"Invalid date format: {data['date']}")
            return False
        
        # Validate series_id if present
        if 'series_id' in data and not data['series_id']:
            self.logger.warning("Empty series_id")
            return False
            
        return True


    def get_economic_indicators(self):
        """Get relevant economic indicators that affect commodity prices"""
        if not self.api_key:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        indicators = {
            # Macroeconomic indicators
            'GDP': 'GDPC1',               # Real Gross Domestic Product
            'GDP_Growth': 'A191RL1Q225SBEA',  # Real Gross Domestic Product, Percent Change From Preceding Period
            'Nominal_GDP': 'GDP',         # Gross Domestic Product, Billions of Dollars
            'CPI': 'CPIAUCSL',            # Consumer Price Index for All Urban Consumers
            'Core_CPI': 'CPILFESL',       # Consumer Price Index for All Urban Consumers: Less Food & Energy
            'PPI': 'PPIACO',              # Producer Price Index for All Commodities
            'Industrial_Production': 'INDPRO',  # Industrial Production: Total Index
            # Employment indicators
            'Unemployment': 'UNRATE',     # Unemployment Rate
            'Employment': 'PAYEMS',       # All Employees, Total Nonfarm
            'Manufacturing_Employment': 'MANEMP',  # All Employees, Manufacturing
            'Unemployment_Rate': 'UNRATE',  # Civilian Unemployment Rate
            'Labor_Force_Participation': 'CIVPART',  # Civilian Labor Force Participation Rate
            'Average_Hourly_Earnings': 'CES0500000003',  # Average Hourly Earnings of All Employees, Total Private
            # Financial indicators
            'Federal_Funds_Rate': 'FEDFUNDS',  # Federal Funds Effective Rate
            '10Y_Treasury_Rate': 'DGS10',  # 10-Year Treasury Constant Maturity Rate
            '3M_Treasury_Rate': 'DGS3MO',  # 3-Month Treasury Bill: Secondary Market Rate
            'Corporate_Bond_Yield': 'BAA',  # Moody's Seasoned Baa Corporate Bond Yield
            'TED_Spread': 'TEDRATE',       # TED Spread
            # Money supply indicators
            'M1_Money_Supply': 'M1SL',    # M1 Money Stock
            'M2_Money_Supply': 'M2SL',    # M2 Money Stock
            'M3_Money_Supply': 'M3SL',    # M3 Money Stock (Discontinued)
            # Exchange rates
            'Dollar_Index': 'DTWEXBGS',   # Trade Weighted U.S. Dollar Index: Broad, Goods and Services
            'Euro_USD': 'DEXUSEU',        # U.S. / Euro Foreign Exchange Rate
            'Yen_USD': 'DEXJPUS',         # Japan / U.S. Foreign Exchange Rate
            'Yuan_USD': 'DEXCHUS',        # China / U.S. Foreign Exchange Rate
            'Pound_USD': 'DEXUSUK',       # U.S. / U.K. Foreign Exchange Rate
            # Housing indicators
            'Case_Shiller_Index': 'CSUSHPINSA',  # S&P/Case-Shiller U.S. National Home Price Index
            'Housing_Starts': 'HOUST',    # Housing Starts: Total: New Privately Owned Housing Units Started
            'Existing_Home_Sales': 'EXHOSLUSM495S',  # Existing Home Sales
            # Consumer indicators
            'Consumer_Spending': 'PCEC',  # Personal Consumption Expenditures
            'Retail_Sales': 'RSXFS',      # Retail Sales, Excluding Food Services
            'Consumer_Confidence': 'UMCSENT',  # University of Michigan: Consumer Sentiment
            # Trade indicators
            'Trade_Balance': 'BOPGSTB',   # Balance on Goods and Services, Trade Balance
            'Exports': 'EXPGSC1',         # Exports of Goods and Services
            'Imports': 'IMPGSC1',         # Imports of Goods and Services
            # Volatility indicators
            'VIX': 'VIXCLS',              # CBOE Volatility Index: VIX
            # Additional economic indicators
            'Inflation_Rate': 'FPCPITOTLZGUSA',  # Inflation consumer prices annual percentage for United States
            'Stock_Market_Index': 'SP500',  # S&P 500
            # Additional financial indicators
            '10Y_Breakeven_Inflation': 'T10YIE',  # 10-Year Breakeven Inflation Rate
            'High_Yield_Spread': 'BAMLH0A0HYM2',  # ICE BofA US High Yield Index Option-Adjusted Spread
            'NASDAQ_Composite': 'NASDAQCOM',  # NASDAQ Composite Index
            # Additional employment indicators
            'Manufacturing_PMI': 'ISMMPM400SFRBSF',  # ISM Manufacturing: PMI Composite Index
            # Additional consumer indicators
            'University_of_Michigan_Inflation_Expectations': 'MICH',  # University of Michigan Inflation Expectations
            # Additional housing indicators
            'House_Price_Index': 'USSTHPI',  # FHFA House Price Index
            # Additional trade indicators
            'Foreign_Direct_Investment': 'ROWFDI01USQ027S',  # Foreign Direct Investment in the United States
            # Additional macroeconomic indicators
            'Capacity_Utilization': 'CAPUTLG2211S',  # Capacity Utilization: Manufacturing
            'Business_Inventories': 'CBUS',  # Business Inventories
            'New_Private_Housing_Permits': 'PERMIT',  # New Private Housing Units Authorized by Building Permits
            # Additional financial indicators
            '30Y_Conventional_Mortgage_Rate': 'MORTGAGE30US',  # 30-Year Fixed Rate Mortgage Average in the United States
            'Total_Assets_of_Commercial_Banks': 'TOTALSL',  # Total Assets: Total Assets for all Commercial Banks
            # Additional employment indicators
            'Job_Openings': 'JTSJOL',  # Job Openings: Total Nonfarm
            'Total_Nonfarm_Payrolls': 'PAYEMS',  # All Employees, Total Nonfarm
            # Additional consumer indicators
            'Motor_Vehicle_Retail_Sales': 'MRTVSACSGFNS',  # Motor Vehicle Retail Sales: Domestic and Foreign Autos
            'Restaurant_and_Bar_Sales': 'SASPNFSGFRS',  # Advance Real Retail and Food Services Sales: Retail Trade and Food Services
            # Additional trade indicators
            'Trade_Balance_Goods': 'BOPGSTBGS',  # Balance on Goods and Services: Goods
            'Trade_Balance_Services': 'BOPGSTBSS',  # Balance on Goods and Services: Services
        }
        
        results = {}
        
        for name, series_id in indicators.items():
            try:
                url = f"{self.base_url}/series/observations"
                params = {
                    'series_id': series_id,
                    'api_key': self.api_key,
                    'file_type': 'json',
                    'limit': 12,  # Last 12 observations
                    'sort_order': 'desc'
                }
                
                self.logger.info(f"Fetching economic indicator: {name} ({series_id})")
                response = self._make_request(url, params=params)
                
                if response:
                    observations = response.get('observations', [])
                    
                    # Get the latest valid observation
                    for obs in observations:
                        if obs['value'] != '.':
                            results[name] = {
                                'value': float(obs['value']),
                                'date': obs['date'],
                                'series_id': series_id
                            }
                            break
                else:
                    error_msg = f'Failed to get response for {name}'
                    self.logger.error(f"Failed to get {name}: {error_msg}")
                    results[name] = {'error': error_msg}
                            
            except requests.exceptions.Timeout:
                error_msg = f'Timeout error getting {name}'
                self.logger.error(error_msg)
                results[name] = {'error': error_msg}
            except requests.exceptions.RequestException as e:
                error_msg = f'Request error getting {name}: {str(e)}'
                self.logger.error(error_msg)
                results[name] = {'error': error_msg}
            except Exception as e:
                error_msg = f'Unexpected error getting {name}: {str(e)}'
                self.logger.error(error_msg)
                results[name] = {'error': error_msg}
        
        success_count = len([r for r in results.values() if 'error' not in r])
        self.logger.info(f"Retrieved {success_count} of {len(indicators)} economic indicators")
        
        # Save economic indicators data
        economic_data = {
            'collected_at': datetime.utcnow().isoformat(),
            'indicators': results,
            'count': success_count
        }
        self.save_data_to_file(economic_data, "economic_indicators.json", data_type='economic_indicator')
        
        return {
            'success': True,
            'indicators': results,
            'count': success_count
        }
    
    def search_commodity_series(self, search_term):
        """Search for FRED series related to a commodity"""
        if not self.api_key:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            url = f"{self.base_url}/series/search"
            params = {
                'search_text': search_term,
                'api_key': self.api_key,
                'file_type': 'json',
                'limit': 20,
                'order_by': 'popularity',
                'sort_order': 'desc'
            }
            
            self.logger.info(f"Searching FRED series for: {search_term}")
            response = self._make_request(url, params=params)
            
            if response:
                seriess = response.get('seriess', [])
                
                # Filter for price-related series
                price_series = []
                for series in seriess:
                    title = series.get('title', '').lower()
                    if 'price' in title or 'index' in title or search_term.lower() in title:
                        price_series.append({
                            'id': series.get('id'),
                            'title': series.get('title'),
                            'frequency': series.get('frequency'),
                            'units': series.get('units'),
                            'seasonal_adjustment': series.get('seasonal_adjustment'),
                            'popularity': series.get('popularity'),
                            'observation_start': series.get('observation_start'),
                            'observation_end': series.get('observation_end')
                        })
                
                self.logger.info(f"Found {len(price_series)} relevant series for {search_term}")
                
                # Save search results
                search_data = {
                    'search_term': search_term,
                    'collected_at': datetime.utcnow().isoformat(),
                    'series': price_series,
                    'total_found': len(seriess),
                    'filtered_count': len(price_series)
                }
                filename = f"search_results_{search_term.lower().replace(' ', '_')}.json"
                self.save_data_to_file(search_data, filename, data_type='search_result')
                
                return {
                    'success': True,
                    'series': price_series,
                    'total_found': len(seriess),
                    'filtered_count': len(price_series)
                }
            else:
                error_msg = f'Failed to get response from FRED API for search term: {search_term}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = f'Search timeout for {search_term}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f'Search request error for {search_term}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f'Unexpected error searching for {search_term}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
    def collect_all_fred_data(self):
        """Collect all available FRED data including commodities, economic indicators, and metadata"""
        self.logger.info("Starting comprehensive FRED data collection")
        
        # Collect all commodities data
        commodities_result = self.collect_all_commodities_data()
        
        # Collect economic indicators
        indicators_result = self.get_economic_indicators()
        
        # Collect metadata for all series
        series_metadata = {}
        for commodity_name, series_id in self.commodity_series.items():
            metadata = self.get_series_info(series_id)
            if metadata:
                series_metadata[series_id] = metadata
                # Save individual metadata file
                metadata_filename = f"{commodity_name}_metadata.json"
                self.save_data_to_file(metadata, metadata_filename, data_type='metadata')
        
        # Save all metadata to a single file
        all_metadata = {
            'collected_at': datetime.utcnow().isoformat(),
            'series_metadata': series_metadata
        }
        self.save_data_to_file(all_metadata, "all_series_metadata.json", data_type='metadata')
        
        # Perform searches for additional series
        search_terms = ['gold', 'silver', 'lithium', 'platinum', 'palladium', 
                       'cobalt', 'molybdenum', 'tungsten', 'vanadium', 'manganese',
                       'chromium', 'antimony', 'titanium', 'magnesium', 'zirconium',
                       'hafnium', 'gallium', 'indium', 'germanium', 'rare earth',
                       'nickel pig iron', 'ferroalloys', 'scandium', 'niobium',
                       'ruthenium', 'rhodium', 'iridium', 'osmium', 'copper concentrate',
                       'lithium carbonate', 'lithium hydroxide', 'cobalt sulfate',
                       'nickel matte', 'nickel ore', 'aluminum alloy', 'aluminum ingot',
                       'steel rebar', 'steel coil', 'steel plate', 'iron ore fines',
                       'neodymium', 'praseodymium', 'lanthanum', 'cerium', 'europium',
                       'gadolinium', 'terbium', 'dysprosium', 'holmium', 'erbium',
                       'thulium', 'ytterbium', 'lutetium', 'yttrium', 'samarium',
                       'promethium', 'samarium-cobalt', 'neodymium-iron-boron',
                       'permanent magnets', 'electric vehicle batteries',
                       'battery grade lithium', 'battery grade cobalt', 'battery grade nickel',
                       'graphite anode', 'silicon carbide', 'gallium arsenide',
                       'indium tin oxide', 'tellurium', 'selenium', 'cadmium',
                       'bismuth', 'tantalum', 'niobium', 'beryllium',
                       'propane', 'heating oil', 'diesel', 'jet fuel', 'gasoline',
                       'palm oil', 'soybean oil', 'rapeseed oil',
                       'commodity index', 'CRB Index', 'GSCI']
        search_results = {}
        for term in search_terms:
            search_result = self.search_commodity_series(term)
            if search_result['success']:
                search_results[term] = search_result
                
        self.logger.info("Completed comprehensive FRED data collection")
        
        return {
            'success': True,
            'commodities': commodities_result,
            'economic_indicators': indicators_result,
            'series_metadata': series_metadata,
            'search_results': search_results
        }

    def collect_historical_data(self, commodity_name, start_year=1990, end_year=2025):
        """Collect historical data for a specific commodity over a range of years"""
        if commodity_name not in self.commodity_series:
            error_msg = f"Commodity {commodity_name} not found in series mapping"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        series_id = self.commodity_series[commodity_name]
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        
        self.logger.info(f"Collecting historical data for {commodity_name} from {start_date} to {end_date}")
        result = self.collect_price_data(commodity_name, start_date=start_date, end_date=end_date)
        
        if result['success']:
            # Save historical data to file
            filename = f"{commodity_name}_historical_data_{start_year}_{end_year}.json"
            self.save_data_to_file(result, filename, data_type='commodity', commodity_name=commodity_name)
            
            self.logger.info(f"Saved historical data for {commodity_name} with {result['count']} records")
            return result
        else:
            self.logger.error(f"Failed to collect historical data for {commodity_name}: {result['error']}")
            return result

    def collect_all_historical_data(self, start_year=1990, end_year=2025):
        """Collect historical data for all commodities"""
        all_historical_data = {}
        
        for commodity_name in self.commodity_series.keys():
            self.logger.info(f"Collecting historical data for {commodity_name}")
            result = self.collect_historical_data(commodity_name, start_year, end_year)
            
            if result['success']:
                all_historical_data[commodity_name] = result
                self.logger.info(f"Successfully collected historical data for {commodity_name}")
            else:
                self.logger.error(f"Failed to collect historical data for {commodity_name}: {result['error']}")
        
        return {
            'success': True,
            'data': all_historical_data,
            'total_commodities': len(all_historical_data)
        }

    def save_data_to_file(self, data, filename, data_type='general', commodity_name=None):
        """Save data to a JSON file in an organized directory structure"""
        try:
            # Determine the appropriate directory based on data type
            if data_type == 'commodity' and commodity_name:
                # Save commodity data in commodity-specific directory
                commodity_dir = os.path.join(self.commodities_dir, commodity_name.lower())
                filepath = os.path.join(commodity_dir, filename)
            elif data_type == 'economic_indicator':
                # Save economic indicators in dedicated directory
                filepath = os.path.join(self.economic_indicators_dir, filename)
            elif data_type == 'metadata':
                # Save metadata in dedicated directory
                filepath = os.path.join(self.metadata_dir, filename)
            elif data_type == 'search_result':
                # Save search results in dedicated directory
                filepath = os.path.join(self.search_results_dir, filename)
            else:
                # Default to main data directory
                filepath = os.path.join(self.data_dir, filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save data to file
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving data to {filename}: {e}")
            return False
    
    def collect_all_commodities_data(self):
        """Collect price data for all commodities and save to files"""
        all_data = []
        
        for commodity_name in self.commodity_series.keys():
            self.logger.info(f"Collecting data for {commodity_name}")
            result = self.collect_price_data(commodity_name)
            
            if result['success']:
                # Save commodity data to file in organized structure
                filename = f"{commodity_name}_data.json"
                self.save_data_to_file(result, filename, data_type='commodity', commodity_name=commodity_name)
                
                # Add to all data
                all_data.extend(result['data'])
                
                self.logger.info(f"Collected {result['count']} records for {commodity_name}")
            else:
                self.logger.error(f"Failed to collect data for {commodity_name}: {result['error']}")
        
        # Save all data to a single file
        all_filename = "all_commodities_data.json"
        self.save_data_to_file({
            'collected_at': datetime.utcnow().isoformat(),
            'total_records': len(all_data),
            'data': all_data
        }, all_filename, data_type='general')
        
        return {
            'success': True,
            'data': all_data,
            'total_records': len(all_data)
        }

