import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .fred_collector import FREDCollector
from .worldbank_collector import WorldBankCollector
from .usgs_collector import USGSCollector
from ..models.user import db
from ..models.commodity import Commodity
from ..models.country import Country
from ..models.production_data import ProductionData
from ..models.reserves_data import ReservesData
from ..models.price_data import PriceData
from ..models.data_source import DataSource

class DataCollectionService:
    """Service to orchestrate data collection from multiple sources"""
    
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)
        
        # Initialize collectors
        self.collectors = {
            'fred': FREDCollector(),
            'worldbank': WorldBankCollector(),
            'usgs': USGSCollector()
        }
        
        # Collection status
        self.collection_status = {
            'last_run': None,
            'running': False,
            'errors': []
        }
    
    def initialize_data_sources(self):
        """Initialize data sources in the database"""
        with self.app.app_context():
            sources = [
                {
                    'name': 'Federal Reserve Economic Data (FRED)',
                    'url': 'https://fred.stlouisfed.org/',
                    'api_endpoint': 'https://api.stlouisfed.org/fred',
                    'update_frequency': 'daily',
                    'reliability_score': 0.95
                },
                {
                    'name': 'World Bank Open Data',
                    'url': 'https://data.worldbank.org/',
                    'api_endpoint': 'https://api.worldbank.org/v2',
                    'update_frequency': 'annual',
                    'reliability_score': 0.90
                },
                {
                    'name': 'USGS Mineral Commodity Summaries',
                    'url': 'https://www.usgs.gov/centers/nmic',
                    'update_frequency': 'annual',
                    'reliability_score': 0.98
                }
            ]
            
            for source_data in sources:
                existing = DataSource.query.filter_by(name=source_data['name']).first()
                if not existing:
                    source = DataSource(**source_data)
                    db.session.add(source)
            
            db.session.commit()
            self.logger.info("Data sources initialized")
    
    def initialize_commodities(self):
        """Initialize commodities in the database"""
        with self.app.app_context():
            commodities = [
                {'name': 'Copper', 'symbol': 'CU', 'category': 'Base Metal', 'strategic_importance': 9},
                {'name': 'Gold', 'symbol': 'AU', 'category': 'Precious Metal', 'strategic_importance': 8},
                {'name': 'Silver', 'symbol': 'AG', 'category': 'Precious Metal', 'strategic_importance': 7},
                {'name': 'Aluminum', 'symbol': 'AL', 'category': 'Base Metal', 'strategic_importance': 9},
                {'name': 'Nickel', 'symbol': 'NI', 'category': 'Base Metal', 'strategic_importance': 8},
                {'name': 'Zinc', 'symbol': 'ZN', 'category': 'Base Metal', 'strategic_importance': 7},
                {'name': 'Lead', 'symbol': 'PB', 'category': 'Base Metal', 'strategic_importance': 6},
                {'name': 'Lithium', 'symbol': 'LI', 'category': 'Critical Metal', 'strategic_importance': 10},
                {'name': 'Cobalt', 'symbol': 'CO', 'category': 'Critical Metal', 'strategic_importance': 9},
                {'name': 'Rare Earth Elements', 'symbol': 'REE', 'category': 'Critical Metal', 'strategic_importance': 10}
            ]
            
            for commodity_data in commodities:
                existing = Commodity.query.filter_by(name=commodity_data['name']).first()
                if not existing:
                    commodity = Commodity(**commodity_data)
                    db.session.add(commodity)
            
            db.session.commit()
            self.logger.info("Commodities initialized")
    
    def initialize_countries(self):
        """Initialize major mining countries in the database"""
        with self.app.app_context():
            countries = [
                {'name': 'China', 'iso_code': 'CHN', 'continent': 'Asia', 'political_stability_score': 0.75},
                {'name': 'United States', 'iso_code': 'USA', 'continent': 'North America', 'political_stability_score': 0.85},
                {'name': 'Australia', 'iso_code': 'AUS', 'continent': 'Oceania', 'political_stability_score': 0.95},
                {'name': 'Chile', 'iso_code': 'CHL', 'continent': 'South America', 'political_stability_score': 0.80},
                {'name': 'Peru', 'iso_code': 'PER', 'continent': 'South America', 'political_stability_score': 0.70},
                {'name': 'Canada', 'iso_code': 'CAN', 'continent': 'North America', 'political_stability_score': 0.95},
                {'name': 'Russia', 'iso_code': 'RUS', 'continent': 'Europe', 'political_stability_score': 0.60},
                {'name': 'South Africa', 'iso_code': 'ZAF', 'continent': 'Africa', 'political_stability_score': 0.65},
                {'name': 'Brazil', 'iso_code': 'BRA', 'continent': 'South America', 'political_stability_score': 0.75},
                {'name': 'Indonesia', 'iso_code': 'IDN', 'continent': 'Asia', 'political_stability_score': 0.70}
            ]
            
            for country_data in countries:
                existing = Country.query.filter_by(iso_code=country_data['iso_code']).first()
                if not existing:
                    country = Country(**country_data)
                    db.session.add(country)
            
            db.session.commit()
            self.logger.info("Countries initialized")
    
    def collect_all_data(self):
        """Collect data from all sources"""
        if self.collection_status['running']:
            self.logger.warning("Data collection already running")
            return
        
        self.collection_status['running'] = True
        self.collection_status['errors'] = []
        start_time = datetime.utcnow()
        
        try:
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                
                # Submit collection tasks
                futures.append(executor.submit(self._collect_fred_data))
                futures.append(executor.submit(self._collect_worldbank_data))
                futures.append(executor.submit(self._collect_usgs_data))
                
                # Wait for completion
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        self.logger.info(f"Collection completed: {result}")
                    except Exception as e:
                        self.logger.error(f"Collection failed: {e}")
                        self.collection_status['errors'].append(str(e))
        
        except Exception as e:
            self.logger.error(f"Data collection service error: {e}")
            self.collection_status['errors'].append(str(e))
        
        finally:
            self.collection_status['running'] = False
            self.collection_status['last_run'] = start_time.isoformat()
    
    def _collect_fred_data(self):
        """Collect data from FRED"""
        try:
            collector = self.collectors['fred']
            data = collector.collect_data()
            
            with self.app.app_context():
                self._store_price_data(data, 'FRED')
            
            return f"FRED: {len(data)} records collected"
        
        except Exception as e:
            self.logger.error(f"FRED collection error: {e}")
            raise
    
    def _collect_worldbank_data(self):
        """Collect data from World Bank"""
        try:
            collector = self.collectors['worldbank']
            data = collector.collect_data()
            
            with self.app.app_context():
                self._store_worldbank_data(data)
            
            return f"World Bank: {len(data)} records collected"
        
        except Exception as e:
            self.logger.error(f"World Bank collection error: {e}")
            raise
    
    def _collect_usgs_data(self):
        """Collect data from USGS"""
        try:
            collector = self.collectors['usgs']
            # Collect historical data going back to 1900 for all major commodities
            data = collector.collect_historical_data()
            
            with self.app.app_context():
                self._store_usgs_data(data)
            
            return f"USGS: {len(data)} records collected"
        
        except Exception as e:
            self.logger.error(f"USGS collection error: {e}")
            raise
    
    def _store_price_data(self, data: List[Dict], source_name: str):
        """Store price data in the database"""
        source = DataSource.query.filter_by(name__icontains=source_name).first()
        if not source:
            return
        
        for item in data:
            # Find commodity
            commodity = Commodity.query.filter_by(name__icontains=item['commodity']).first()
            if not commodity:
                continue
            
            # Create price data entry
            price_data = PriceData(
                commodity_id=commodity.id,
                price=item.get('price'),
                currency=item.get('currency', 'USD'),
                timestamp=datetime.strptime(item['date'], '%Y-%m-%d'),
                data_source_id=source.id
            )
            
            db.session.add(price_data)
        
        db.session.commit()
    
    def _store_worldbank_data(self, data: List[Dict]):
        """Store World Bank data in the database"""
        # Implementation would depend on the specific data structure
        pass
    
    def _store_usgs_data(self, data: List[Dict]):
        """Store USGS data in the database"""
        if not data:
            return
            
        # Get the USGS data source
        source = DataSource.query.filter(DataSource.name.like('%USGS%')).first()
        if not source:
            self.logger.warning("USGS data source not found in database")
            return
        
        # Get all commodities and countries for quick lookup
        commodities = {c.name.lower(): c.id for c in Commodity.query.all()}
        countries = {c.name.lower(): c.id for c in Country.query.all()}
        
        production_records = 0
        reserves_records = 0
        
        for item in data:
            # Skip items without required data
            if not item.get('commodity') or not item.get('year'):
                continue
                
            # Find commodity
            commodity_name = item['commodity'].lower()
            if commodity_name not in commodities:
                # Try to find a close match
                for db_commodity_name in commodities:
                    if commodity_name in db_commodity_name or db_commodity_name in commodity_name:
                        commodity_name = db_commodity_name
                        break
                else:
                    self.logger.warning(f"Commodity not found in database: {item['commodity']}")
                    continue
                    
            commodity_id = commodities[commodity_name]
            
            # Find country
            country_name = item.get('country', '').lower()
            if not country_name or country_name not in countries:
                # Default to USA if no country specified
                country_id = countries.get('united states', None)
                if not country_id:
                    continue
            else:
                country_id = countries[country_name]
            
            year = item['year']
            
            # Store production data if available
            if 'production_volume' in item and item['production_volume'] is not None:
                # Check if record already exists
                existing = ProductionData.query.filter_by(
                    commodity_id=commodity_id,
                    country_id=country_id,
                    year=year,
                    data_source_id=source.id
                ).first()
                
                if not existing:
                    production_data = ProductionData(
                        commodity_id=commodity_id,
                        country_id=country_id,
                        year=year,
                        production_volume=item['production_volume'],
                        unit=item.get('unit', 'metric tons'),
                        data_source_id=source.id,
                        validation_status='pending'
                    )
                    db.session.add(production_data)
                    production_records += 1
            
            # Store reserves data if available
            if 'reserves_volume' in item and item['reserves_volume'] is not None:
                # Check if record already exists
                existing = ReservesData.query.filter_by(
                    commodity_id=commodity_id,
                    country_id=country_id,
                    year=year,
                    data_source_id=source.id
                ).first()
                
                if not existing:
                    reserves_data = ReservesData(
                        commodity_id=commodity_id,
                        country_id=country_id,
                        year=year,
                        reserves_volume=item['reserves_volume'],
                        unit=item.get('unit', 'metric tons'),
                        data_source_id=source.id,
                        validation_status='pending'
                    )
                    db.session.add(reserves_data)
                    reserves_records += 1
        
        try:
            db.session.commit()
            self.logger.info(f"Stored USGS data: {production_records} production records, {reserves_records} reserves records")
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error storing USGS data: {e}")
    
    def schedule_collections(self):
        """Schedule regular data collections"""
        # Schedule FRED data collection (daily)
        schedule.every().day.at("06:00").do(self._collect_fred_data)
        
        # Schedule World Bank data collection (weekly)
        schedule.every().monday.at("07:00").do(self._collect_worldbank_data)
        
        # Schedule USGS data collection (monthly)
        schedule.every().month.do(self._collect_usgs_data)
        
        self.logger.info("Data collection scheduled")
    
    def run_scheduler(self):
        """Run the scheduler (should be run in a separate thread/process)"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def get_collection_status(self) -> Dict[str, Any]:
        """Get current collection status"""
        return self.collection_status.copy()
    
    def force_collection(self, source: str = None):
        """Force immediate data collection"""
        if source:
            if source == 'fred':
                return self._collect_fred_data()
            elif source == 'worldbank':
                return self._collect_worldbank_data()
            elif source == 'usgs':
                return self._collect_usgs_data()
            else:
                raise ValueError(f"Unknown source: {source}")
        else:
            return self.collect_all_data()

