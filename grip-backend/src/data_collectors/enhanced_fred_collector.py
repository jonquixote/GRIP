"""
Enhanced FRED Collector using fredapi library
"""

import os
import pandas as pd
import json
import logging
from datetime import datetime
from fredapi import Fred
from .base_collector import BaseDataCollector

class EnhancedFREDCollector(BaseDataCollector):
    def __init__(self):
        super().__init__(name="EnhancedFRED", base_url="https://api.stlouisfed.org/fred")
        # Get API key from environment variable
        self.api_key = os.getenv('FRED_API_KEY')
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'fred_enhanced')
        
        # Set up logging
        self.logger = logging.getLogger(f"collector.{self.name}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        # Initialize fredapi client
        if self.api_key:
            self.fred = Fred(api_key=self.api_key)
        else:
            self.fred = None
            self.logger.error("No FRED API key configured")
        
        # Enhanced commodity series mapping with more series
        self.commodity_series = {
            # Base metals
            'copper': 'PCOPPUSDM',        # Global price of Copper, U.S. Dollars per Metric Ton
            'aluminum': 'PALUMUSDM',      # Global price of Aluminum, U.S. Dollars per Metric Ton
            'nickel': 'PNICKUSDM',        # Global price of Nickel, U.S. Dollars per Metric Ton
            'zinc': 'PZINCUSDM',          # Global price of Zinc, U.S. Dollars per Metric Ton
            'lead': 'PLEADUSDM',          # Global price of Lead, U.S. Dollars per Metric Ton
            'tin': 'PTINUSDQ',            # Global price of Tin, U.S. Dollars per Metric Ton (quarterly)
            # Precious metals
            'gold': 'XAUUSD',             # Gold Fixing Price 10:30 A.M. (London Gold Market) in London/British Pound
            'silver': 'XAGUSD',           # Silver Price: USD troy oz
            'platinum': 'XPTUSD',         # Platinum Fixing Price 10:30 A.M. (London Platinum Market) in London/USD
            'palladium': 'XPDUSD',        # Palladium Fixing Price 10:30 A.M. (London Platinum and Palladium Market) in London/USD
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
            # Additional industrial metals
            'molybdenum': 'PMOUSD',       # Molybdenum Price, U.S. Dollars per Metric Ton
            'tungsten': 'PTUUSD',         # Tungsten Price, U.S. Dollars per Metric Ton
            'vanadium': 'PVUSD',          # Vanadium Price, U.S. Dollars per Metric Ton
            'cobalt': 'PCOUSD',           # Cobalt Price, U.S. Dollars per Metric Ton
            'titanium': 'PTIUSD',         # Titanium Price, U.S. Dollars per Metric Ton
            # Additional agricultural commodities
            'soybean_oil': 'PSBOUSD',     # Soybean Oil Price, U.S. Dollars per Metric Ton
            'rapeseed_oil': 'PRSOUSD',    # Rapeseed Oil Price, U.S. Dollars per Metric Ton
            # Additional energy commodities
            'lng': 'PLNGUSD',             # Liquefied Natural Gas Price, U.S. Dollars per Metric Ton
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
        self.revisions_dir = os.path.join(self.data_dir, 'revisions')
        self.categories_dir = os.path.join(self.data_dir, 'categories')
        self.releases_dir = os.path.join(self.data_dir, 'releases')
        
        # Create all subdirectories
        for directory in [self.commodities_dir, self.economic_indicators_dir, 
                         self.metadata_dir, self.search_results_dir, 
                         self.revisions_dir, self.categories_dir, self.releases_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create commodity-specific directories
        for commodity in self.commodity_series.keys():
            commodity_dir = os.path.join(self.commodities_dir, commodity)
            os.makedirs(commodity_dir, exist_ok=True)
        
    def test_connection(self):
        """Test FRED API connection"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            # Test with a simple series request
            self.logger.info("Testing FRED API connection")
            data = self.fred.get_series_info('GDP')
            
            if data is not None:
                success_msg = 'FRED API connection successful'
                self.logger.info(success_msg)
                return {
                    'success': True, 
                    'message': success_msg,
                    'test_series': data['title'] if 'title' in data else 'Unknown',
                    'api_key_valid': True
                }
            else:
                error_msg = 'Unexpected API response format or empty response'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
        except Exception as e:
            error_msg = f'Error testing FRED API connection: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
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
    
    def get_series_latest_release(self, series_id):
        """Get latest data for a Fred series id. This is equivalent to get_series()"""
        if not self.fred:
            return None
        try:
            return self.fred.get_series(series_id)
        except Exception as e:
            self.logger.error(f"Error getting latest release for {series_id}: {e}")
            return None
    
    def get_series_info(self, series_id):
        """Get metadata about a FRED series"""
        if not self.fred:
            self.logger.warning("No API key available for series info request")
            return None
        
        try:
            self.logger.info(f"Fetching series info for {series_id}")
            data = self.fred.get_series_info(series_id)
            
            if data is not None:
                # Convert pandas Series to dictionary
                if isinstance(data, pd.Series):
                    return data.to_dict()
                return data
            else:
                self.logger.warning(f"Unexpected response format for series info: {series_id}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error getting series info for {series_id}: {e}")
            return None
    
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

    def collect_all_fred_data(self):
        """Collect all available FRED data comprehensively"""
        self.logger.info("Starting comprehensive FRED data collection")
        
        # Collect all commodities data with full details
        self.logger.info("Collecting all commodities data...")
        commodities_result = self.collect_all_commodities_data_comprehensive()
        
        # Collect economic indicators
        self.logger.info("Collecting economic indicators...")
        indicators_result = self.get_economic_indicators()
        
        # Collect metadata for all series
        self.logger.info("Collecting metadata for all series...")
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
        
        # Collect revisions data for all series
        self.logger.info("Collecting revision data for all series...")
        revisions_data = {}
        for commodity_name, series_id in self.commodity_series.items():
            try:
                # Get all releases
                all_releases = self.fred.get_series_all_releases(series_id)
                if all_releases is not None and not all_releases.empty:
                    # Process all releases data
                    releases_data = []
                    for _, row in all_releases.iterrows():
                        if pd.notna(row['value']):
                            releases_data.append({
                                'realtime_start': row['realtime_start'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(row['realtime_start'], 'strftime') else str(row['realtime_start']),
                                'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
                                'value': float(row['value']),
                                'series_id': series_id
                            })
                    
                    revisions_data[f"{series_id}_all_releases"] = {
                        'count': len(releases_data),
                        'data': releases_data
                    }
                    
                    # Save individual releases file
                    releases_filename = f"{commodity_name}_all_releases.json"
                    self.save_data_to_file({
                        'collected_at': datetime.utcnow().isoformat(),
                        'series_id': series_id,
                        'commodity': commodity_name,
                        'data': releases_data,
                        'count': len(releases_data)
                    }, releases_filename, data_type='revisions')
                
                # Get first release
                first_release = self.fred.get_series_first_release(series_id)
                if first_release is not None and not first_release.empty:
                    # Process first release data
                    first_release_data = []
                    for date, value in first_release.items():
                        if pd.notna(value):
                            first_release_data.append({
                                'date': date.strftime('%Y-%m-%d'),
                                'value': float(value),
                                'series_id': series_id
                            })
                    
                    revisions_data[f"{series_id}_first_release"] = {
                        'count': len(first_release_data),
                        'data': first_release_data
                    }
                    
                    # Save individual first release file
                    first_release_filename = f"{commodity_name}_first_release.json"
                    self.save_data_to_file({
                        'collected_at': datetime.utcnow().isoformat(),
                        'series_id': series_id,
                        'commodity': commodity_name,
                        'data': first_release_data,
                        'count': len(first_release_data)
                    }, first_release_filename, data_type='revisions')
                
                # Get vintage dates
                try:
                    vintage_dates = self.fred.get_series_vintage_dates(series_id)
                    if vintage_dates is not None:
                        vintage_dates_str = [date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(date, 'strftime') else str(date) for date in vintage_dates[:50]]
                        revisions_data[f"{series_id}_vintage_dates"] = {
                            'count': len(vintage_dates_str),
                            'dates': vintage_dates_str
                        }
                        
                        # Save individual vintage dates file
                        vintage_filename = f"{commodity_name}_vintage_dates.json"
                        self.save_data_to_file({
                            'collected_at': datetime.utcnow().isoformat(),
                            'series_id': series_id,
                            'commodity': commodity_name,
                            'vintage_dates': vintage_dates_str,
                            'count': len(vintage_dates_str)
                        }, vintage_filename, data_type='metadata')
                except Exception as e:
                    self.logger.warning(f"Could not get vintage dates for {commodity_name}: {e}")
                    
            except Exception as e:
                self.logger.error(f"Error collecting revisions for {commodity_name}: {e}")
                continue
        
        # Perform searches for additional series
        self.logger.info("Performing searches for additional relevant data...")
        search_terms = ['commodity prices', 'metals', 'energy', 'agriculture', 'industrial metals']
        search_results = {}
        for term in search_terms:
            try:
                search_result = self.fred.search(term, limit=100)
                if search_result is not None and not search_result.empty:
                    # Convert DataFrame to list of dictionaries
                    search_data = []
                    for _, row in search_result.iterrows():
                        result_entry = {}
                        for col in search_result.columns:
                            result_entry[col] = str(row[col]) if pd.notna(row[col]) else None
                        search_data.append(result_entry)
                    
                    search_results[term] = {
                        'count': len(search_data),
                        'data': search_data
                    }
                    
                    # Save individual search results
                    search_filename = f"search_results_{term.replace(' ', '_')}.json"
                    self.save_data_to_file({
                        'collected_at': datetime.utcnow().isoformat(),
                        'search_term': term,
                        'data': search_data,
                        'count': len(search_data)
                    }, search_filename, data_type='search_result')
            except Exception as e:
                self.logger.error(f"Error searching for {term}: {e}")
                continue
        
        # Search by categories for commodities
        self.logger.info("Searching by categories...")
        category_ids = [1, 3, 32145]  # General, Money & Banking, Industrial Production
        category_results = {}
        for cat_id in category_ids:
            try:
                category_result = self.fred.search_by_category(cat_id, limit=100)
                if category_result is not None and not category_result.empty:
                    # Convert DataFrame to list of dictionaries
                    category_data = []
                    for _, row in category_result.iterrows():
                        result_entry = {}
                        for col in category_result.columns:
                            result_entry[col] = str(row[col]) if pd.notna(row[col]) else None
                        category_data.append(result_entry)
                    
                    category_results[cat_id] = {
                        'count': len(category_data),
                        'data': category_data
                    }
                    
                    # Save individual category results
                    category_filename = f"category_{cat_id}_results.json"
                    self.save_data_to_file({
                        'collected_at': datetime.utcnow().isoformat(),
                        'category_id': cat_id,
                        'data': category_data,
                        'count': len(category_data)
                    }, category_filename, data_type='categories')
            except Exception as e:
                self.logger.error(f"Error searching by category {cat_id}: {e}")
                continue
        
        # Search by releases
        self.logger.info("Searching by releases...")
        release_ids = [175, 226, 151]  # Various economic releases
        release_results = {}
        for rel_id in release_ids:
            try:
                release_result = self.fred.search_by_release(rel_id, limit=100)
                if release_result is not None and not release_result.empty:
                    # Convert DataFrame to list of dictionaries
                    release_data = []
                    for _, row in release_result.iterrows():
                        result_entry = {}
                        for col in release_result.columns:
                            result_entry[col] = str(row[col]) if pd.notna(row[col]) else None
                        release_data.append(result_entry)
                    
                    release_results[rel_id] = {
                        'count': len(release_data),
                        'data': release_data
                    }
                    
                    # Save individual release results
                    release_filename = f"release_{rel_id}_results.json"
                    self.save_data_to_file({
                        'collected_at': datetime.utcnow().isoformat(),
                        'release_id': rel_id,
                        'data': release_data,
                        'count': len(release_data)
                    }, release_filename, data_type='releases')
            except Exception as e:
                self.logger.error(f"Error searching by release {rel_id}: {e}")
                continue
        
        self.logger.info("Completed comprehensive FRED data collection")
        
        return {
            'success': True,
            'commodities': commodities_result,
            'economic_indicators': indicators_result,
            'series_metadata': series_metadata,
            'revisions_data': revisions_data,
            'search_results': search_results,
            'category_results': category_results,
            'release_results': release_results
        }
    
    def collect_price_data(self, commodity_name, start_date=None, end_date=None):
        """Collect price data for a commodity from FRED using fredapi"""
        if not self.fred:
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
            self.logger.info(f"Making request to FRED API for {commodity_name} ({series_id})")
            
            # Get the actual data
            kwargs = {}
            if start_date:
                kwargs['observation_start'] = start_date
            if end_date:
                kwargs['observation_end'] = end_date
                
            data = self.fred.get_series(series_id, **kwargs)
            
            if data is not None and not data.empty:
                # Process the data
                price_data = []
                for date, value in data.items():
                    if pd.notna(value):  # Check for NaN values
                        try:
                            data_point = {
                                'date': date.strftime('%Y-%m-%d'),
                                'price': float(value),
                                'commodity': commodity_name,
                                'source': 'FRED',
                                'series_id': series_id
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
                
        except Exception as e:
            error_msg = f'Error collecting data for {commodity_name}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_series_latest_release(self, series_id):
        """Get latest data for a Fred series id. This is equivalent to get_series()"""
        if not self.fred:
            return None
        try:
            return self.fred.get_series(series_id)
        except Exception as e:
            self.logger.error(f"Error getting latest release for {series_id}: {e}")
            return None
    
    def get_economic_indicators(self):
        """Get relevant economic indicators that affect commodity prices"""
        if not self.fred:
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
            # Additional consumer indicators
            'University_of_Michigan_Inflation_Expectations': 'MICH',  # University of Michigan Inflation Expectations
            # Additional housing indicators
            'House_Price_Index': 'USSTHPI',  # FHFA House Price Index
            # Additional macroeconomic indicators
            'New_Private_Housing_Permits': 'PERMIT',  # New Private Housing Units Authorized by Building Permits
            # Additional financial indicators
            '30Y_Conventional_Mortgage_Rate': 'MORTGAGE30US',  # 30-Year Fixed Rate Mortgage Average in the United States
            'Total_Assets_of_Commercial_Banks': 'TOTALSL',  # Total Assets: Total Assets for all Commercial Banks
            # Additional employment indicators
            'Job_Openings': 'JTSJOL',  # Job Openings: Total Nonfarm
            'Total_Nonfarm_Payrolls': 'PAYEMS',  # All Employees, Total Nonfarm
        }
        
        results = {}
        
        for name, series_id in indicators.items():
            try:
                self.logger.info(f"Fetching economic indicator: {name} ({series_id})")
                data = self.fred.get_series(series_id, limit=12)  # Last 12 observations
                
                if data is not None and not data.empty:
                    # Get the latest valid observation
                    for date, value in data.items():
                        if pd.notna(value):
                            results[name] = {
                                'value': float(value),
                                'date': date.strftime('%Y-%m-%d'),
                                'series_id': series_id
                            }
                            break
                else:
                    error_msg = f'Failed to get response for {name}'
                    self.logger.error(f"Failed to get {name}: {error_msg}")
                    results[name] = {'error': error_msg}
                            
            except Exception as e:
                error_msg = f'Error getting {name}: {str(e)}'
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
            elif data_type == 'revisions':
                # Save revisions data in dedicated directory
                filepath = os.path.join(self.revisions_dir, filename)
            elif data_type == 'categories':
                # Save categories data in dedicated directory
                filepath = os.path.join(self.categories_dir, filename)
            elif data_type == 'releases':
                # Save releases data in dedicated directory
                filepath = os.path.join(self.releases_dir, filename)
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
    
    def collect_data(self, commodity_id=None, data_type='price'):
        """Collect data from FRED. If commodity_id is None, collect for all commodities."""
        if commodity_id is None:
            # Collect data for all commodities
            return self.collect_all_commodities_data()
        else:
            # For compatibility, we'll just collect for all commodities regardless of commodity_id
            # In a real implementation, you might want to collect for a specific commodity
            return self.collect_all_commodities_data()
    
    def get_all_releases(self, series_id):
        """Get all data for a Fred series id including first releases and all revisions"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Fetching all releases for series {series_id}")
            data = self.fred.get_series_all_releases(series_id)
            
            if data is not None and not data.empty:
                # Convert DataFrame to list of dictionaries
                releases_data = []
                for _, row in data.iterrows():
                    releases_data.append({
                        'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
                        'realtime_start': row['realtime_start'].strftime('%Y-%m-%d') if hasattr(row['realtime_start'], 'strftime') else str(row['realtime_start']),
                        'value': float(row['value']) if pd.notna(row['value']) else None
                    })
                
                # Save revisions data
                filename = f"{series_id}_all_releases.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'series_id': series_id,
                    'data': releases_data,
                    'count': len(releases_data)
                }, filename, data_type='revisions')
                
                self.logger.info(f"Successfully collected {len(releases_data)} releases for {series_id}")
                return {
                    'success': True,
                    'data': releases_data,
                    'series_id': series_id,
                    'count': len(releases_data)
                }
            else:
                error_msg = f'Failed to get releases data for {series_id}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f'Error collecting releases for {series_id}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_first_release(self, series_id):
        """Get first-release data for a Fred series id"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Fetching first release for series {series_id}")
            data = self.fred.get_series_first_release(series_id)
            
            if data is not None and not data.empty:
                # Process the data
                first_release_data = []
                for date, value in data.items():
                    if pd.notna(value):
                        first_release_data.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'value': float(value)
                        })
                
                # Save first release data
                filename = f"{series_id}_first_release.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'series_id': series_id,
                    'data': first_release_data,
                    'count': len(first_release_data)
                }, filename, data_type='revisions')
                
                self.logger.info(f"Successfully collected {len(first_release_data)} first release records for {series_id}")
                return {
                    'success': True,
                    'data': first_release_data,
                    'series_id': series_id,
                    'count': len(first_release_data)
                }
            else:
                error_msg = f'Failed to get first release data for {series_id}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f'Error collecting first release for {series_id}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def search_series(self, text, limit=1000, order_by=None, sort_order=None, filter=None):
        """Do a fulltext search for series in the Fred dataset"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Searching FRED for: {text}")
            data = self.fred.search(text, limit=limit, order_by=order_by, sort_order=sort_order, filter=filter)
            
            if data is not None and not data.empty:
                # Convert DataFrame to list of dictionaries
                search_results = []
                for _, row in data.iterrows():
                    result = {}
                    for col in data.columns:
                        result[col] = str(row[col]) if pd.notna(row[col]) else None
                    search_results.append(result)
                
                # Save search results
                filename = f"search_results_{text.replace(' ', '_')}.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'search_term': text,
                    'data': search_results,
                    'count': len(search_results)
                }, filename, data_type='search_result')
                
                self.logger.info(f"Successfully found {len(search_results)} search results for: {text}")
                return {
                    'success': True,
                    'data': search_results,
                    'search_term': text,
                    'count': len(search_results)
                }
            else:
                self.logger.info(f"No search results found for: {text}")
                return {
                    'success': True,
                    'data': [],
                    'search_term': text,
                    'count': 0
                }
                
        except Exception as e:
            error_msg = f'Error searching for {text}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def search_by_category(self, category_id, limit=1000, order_by=None, sort_order=None, filter=None):
        """Search for series that belongs to a category id"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Searching FRED by category: {category_id}")
            data = self.fred.search_by_category(category_id, limit=limit, order_by=order_by, sort_order=sort_order, filter=filter)
            
            if data is not None and not data.empty:
                # Convert DataFrame to list of dictionaries
                category_results = []
                for _, row in data.iterrows():
                    result = {}
                    for col in data.columns:
                        result[col] = str(row[col]) if pd.notna(row[col]) else None
                    category_results.append(result)
                
                # Save category results
                filename = f"category_{category_id}_results.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'category_id': category_id,
                    'data': category_results,
                    'count': len(category_results)
                }, filename, data_type='categories')
                
                self.logger.info(f"Successfully found {len(category_results)} results for category: {category_id}")
                return {
                    'success': True,
                    'data': category_results,
                    'category_id': category_id,
                    'count': len(category_results)
                }
            else:
                self.logger.info(f"No results found for category: {category_id}")
                return {
                    'success': True,
                    'data': [],
                    'category_id': category_id,
                    'count': 0
                }
                
        except Exception as e:
            error_msg = f'Error searching by category {category_id}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def search_by_release(self, release_id, limit=1000, order_by=None, sort_order=None, filter=None):
        """Search for series that belongs to a release id"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Searching FRED by release: {release_id}")
            data = self.fred.search_by_release(release_id, limit=limit, order_by=order_by, sort_order=sort_order, filter=filter)
            
            if data is not None and not data.empty:
                # Convert DataFrame to list of dictionaries
                release_results = []
                for _, row in data.iterrows():
                    result = {}
                    for col in data.columns:
                        result[col] = str(row[col]) if pd.notna(row[col]) else None
                    release_results.append(result)
                
                # Save release results
                filename = f"release_{release_id}_results.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'release_id': release_id,
                    'data': release_results,
                    'count': len(release_results)
                }, filename, data_type='releases')
                
                self.logger.info(f"Successfully found {len(release_results)} results for release: {release_id}")
                return {
                    'success': True,
                    'data': release_results,
                    'release_id': release_id,
                    'count': len(release_results)
                }
            else:
                self.logger.info(f"No results found for release: {release_id}")
                return {
                    'success': True,
                    'data': [],
                    'release_id': release_id,
                    'count': 0
                }
                
        except Exception as e:
            error_msg = f'Error searching by release {release_id}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_vintage_dates(self, series_id):
        """Get a list of vintage dates for a series"""
        if not self.fred:
            error_msg = 'No FRED API key configured'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        try:
            self.logger.info(f"Fetching vintage dates for series: {series_id}")
            dates = self.fred.get_series_vintage_dates(series_id)
            
            if dates is not None:
                # Convert dates to strings
                vintage_dates = [str(date) for date in dates]
                
                # Save vintage dates
                filename = f"{series_id}_vintage_dates.json"
                self.save_data_to_file({
                    'collected_at': datetime.utcnow().isoformat(),
                    'series_id': series_id,
                    'vintage_dates': vintage_dates,
                    'count': len(vintage_dates)
                }, filename, data_type='metadata')
                
                self.logger.info(f"Successfully collected {len(vintage_dates)} vintage dates for {series_id}")
                return {
                    'success': True,
                    'vintage_dates': vintage_dates,
                    'series_id': series_id,
                    'count': len(vintage_dates)
                }
            else:
                error_msg = f'Failed to get vintage dates for {series_id}'
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f'Error collecting vintage dates for {series_id}: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def collect_all_fred_data(self):
        """Collect all available FRED data including commodities, economic indicators, metadata, and revisions"""
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
        
        # Collect revisions data for key series
        key_series = list(self.commodity_series.values())[:5]  # Limit to first 5 series to avoid API limits
        revisions_data = {}
        for series_id in key_series:
            # Get all releases
            all_releases = self.get_all_releases(series_id)
            if all_releases['success']:
                revisions_data[f"{series_id}_all_releases"] = all_releases
                
            # Get first release
            first_release = self.get_first_release(series_id)
            if first_release['success']:
                revisions_data[f"{series_id}_first_release"] = first_release
                
            # Get vintage dates
            vintage_dates = self.get_vintage_dates(series_id)
            if vintage_dates['success']:
                revisions_data[f"{series_id}_vintage_dates"] = vintage_dates
        
        # Perform searches for additional series
        search_terms = ['commodity prices', 'metals', 'energy', 'agriculture']
        search_results = {}
        for term in search_terms:
            search_result = self.search_series(term, limit=100)
            if search_result['success']:
                search_results[term] = search_result
                
        # Search by categories (example categories for commodities)
        category_ids = [1, 3, 32145]  # General, Money & Banking, Industrial Production
        category_results = {}
        for cat_id in category_ids:
            category_result = self.search_by_category(cat_id, limit=100)
            if category_result['success']:
                category_results[cat_id] = category_result
                
        # Search by releases (example releases)
        release_ids = [151, 175, 226]  # Various economic releases
        release_results = {}
        for rel_id in release_ids:
            release_result = self.search_by_release(rel_id, limit=100)
            if release_result['success']:
                release_results[rel_id] = release_result
        
        self.logger.info("Completed comprehensive FRED data collection")
        
        return {
            'success': True,
            'commodities': commodities_result,
            'economic_indicators': indicators_result,
            'series_metadata': series_metadata,
            'revisions_data': revisions_data,
            'search_results': search_results,
            'category_results': category_results,
            'release_results': release_results
        }