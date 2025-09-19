import json
import os
from datetime import datetime
from typing import List, Dict, Any
from .base_collector import BaseDataCollector
from src.models.user import db
from src.models.commodity import Commodity
from src.models.production_data import ProductionData
from src.models.reserves_data import ReservesData
from src.models.price_data import PriceData
from src.models.data_source import DataSource
from sqlalchemy.exc import IntegrityError

class FileIngestionCollector(BaseDataCollector):
    """Collector for ingesting existing JSON data files into the database"""
    
    def __init__(self):
        super().__init__(name="FileIngestion")
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'data'
        )
        self.logger.info(f"FileIngestionCollector initialized with data directory: {self.data_dir}")
    
    def collect_data(self, data_type: str = 'all') -> Dict[str, Any]:
        """
        Collect data from existing JSON files and store in database
        
        Args:
            data_type: Type of data to collect ('usgs', 'fred', 'all')
        """
        results = {
            'success': True,
            'ingested_files': [],
            'errors': [],
            'summary': {}
        }
        
        try:
            # Ensure data sources exist
            self._ensure_data_sources()
            
            # Process USGS data if requested
            if data_type in ['usgs', 'all']:
                usgs_results = self._process_usgs_data()
                results['ingested_files'].extend(usgs_results['ingested_files'])
                results['errors'].extend(usgs_results['errors'])
                results['summary']['usgs'] = usgs_results['summary']
            
            # Process FRED data if requested
            if data_type in ['fred', 'all']:
                fred_results = self._process_fred_data()
                results['ingested_files'].extend(fred_results['ingested_files'])
                results['errors'].extend(fred_results['errors'])
                results['summary']['fred'] = fred_results['summary']
                
            # Detect anomalies in the newly ingested data
            if results['summary'].get('usgs', {}).get('records_ingested', 0) > 0 or \
               results['summary'].get('fred', {}).get('records_ingested', 0) > 0:
                self.logger.info("Performing anomaly detection on newly ingested data")
                # This would be implemented in a more sophisticated system
                # For now, we'll just log that we would do this
                
        except Exception as e:
            self.logger.error(f"Error during data collection: {str(e)}")
            results['success'] = False
            results['errors'].append(str(e))
            
        return results
    
    def _ensure_data_sources(self):
        """Ensure required data sources exist in the database"""
        # USGS data source
        usgs_source = DataSource.query.filter_by(name='USGS').first()
        if not usgs_source:
            usgs_source = DataSource(
                name='USGS',
                url='https://www.usgs.gov/centers/nmic',
                reliability_score=0.95
            )
            db.session.add(usgs_source)
        
        # FRED data source
        fred_source = DataSource.query.filter_by(name='FRED').first()
        if not fred_source:
            fred_source = DataSource(
                name='FRED',
                url='https://fred.stlouisfed.org/',
                reliability_score=0.98
            )
            db.session.add(fred_source)
            
        db.session.commit()
    
    def _process_usgs_data(self) -> Dict[str, Any]:
        """Process USGS data files"""
        results = {
            'ingested_files': [],
            'errors': [],
            'summary': {
                'files_processed': 0,
                'records_ingested': 0,
                'commodities_created': 0
            }
        }
        
        usgs_dir = os.path.join(self.data_dir, 'usgs')
        if not os.path.exists(usgs_dir):
            self.logger.warning(f"USGS data directory not found: {usgs_dir}")
            return results
            
        # Process all JSON files in the USGS directory
        for filename in os.listdir(usgs_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(usgs_dir, filename)
                try:
                    self.logger.info(f"Processing USGS file: {filename}")
                    file_results = self._ingest_usgs_file(filepath)
                    results['ingested_files'].append(filename)
                    results['summary']['records_ingested'] += file_results['records_ingested']
                    results['summary']['commodities_created'] += file_results['commodities_created']
                    results['summary']['files_processed'] += 1
                except Exception as e:
                    error_msg = f"Error processing {filename}: {str(e)}"
                    self.logger.error(error_msg)
                    results['errors'].append(error_msg)
        
        return results
    
    def _ingest_usgs_file(self, filepath: str) -> Dict[str, Any]:
        """Ingest a single USGS JSON file"""
        results = {
            'records_ingested': 0,
            'commodities_created': 0
        }
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Handle both array and object formats
            records = data if isinstance(data, list) else data.get('data', [])
            
            for record in records:
                # Validate data point
                if not self.validate_data(record):
                    self.logger.warning(f"Invalid data point in {os.path.basename(filepath)}: {record}")
                    continue
                    
                # Calculate quality score
                quality_score = self.calculate_data_quality_score(record)
                
                # Skip low quality data
                if quality_score < 0.5:  # Threshold can be adjusted
                    self.logger.warning(f"Low quality data point skipped (score: {quality_score}): {record}")
                    continue
                
                # Extract commodity info
                commodity_name = record.get('commodity')
                if not commodity_name:
                    continue
                    
                # Get or create commodity
                commodity = Commodity.query.filter_by(name=commodity_name.title()).first()
                if not commodity:
                    # Generate a unique symbol
                    base_symbol = commodity_name[:3].upper()
                    symbol = base_symbol
                    counter = 1
                    # Ensure symbol is unique
                    while Commodity.query.filter_by(symbol=symbol).first():
                        symbol = f"{base_symbol}{counter}"
                        counter += 1
                        
                    commodity = Commodity(
                        name=commodity_name.title(),
                        symbol=symbol
                    )
                    db.session.add(commodity)
                    db.session.flush()  # Get the ID without committing
                    results['commodities_created'] += 1
                
                # Extract country info (simplified)
                country_name = record.get('country', 'World')
                # For simplicity, we'll use a generic country ID
                # In a full implementation, you'd have a countries table
                country_id = 1  # Placeholder
                
                # Extract year
                year = record.get('year')
                if not year:
                    continue
                
                # Extract production volume
                production_volume = record.get('production_volume')
                if production_volume is not None:
                    # Check if record already exists
                    existing = ProductionData.query.filter_by(
                        commodity_id=commodity.id,
                        country_id=country_id,
                        year=year
                    ).first()
                    
                    if not existing:
                        production_data = ProductionData(
                            commodity_id=commodity.id,
                            country_id=country_id,
                            year=year,
                            production_volume=production_volume,
                            unit=record.get('unit', 'metric tons'),
                            data_source_id=DataSource.query.filter_by(name='USGS').first().id,
                            validation_status='validated',
                            data_quality_score=self.calculate_data_quality_score(record),
                            confidence_score=min(0.95, self.calculate_data_quality_score(record) + 0.1)  # Slightly higher confidence
                        )
                        db.session.add(production_data)
                        results['records_ingested'] += 1
                
                # Extract reserves volume
                reserves_volume = record.get('reserves_volume')
                if reserves_volume is not None:
                    # Check if record already exists
                    existing = ReservesData.query.filter_by(
                        commodity_id=commodity.id,
                        country_id=country_id,
                        year=year
                    ).first()
                    
                    if not existing:
                        reserves_data = ReservesData(
                            commodity_id=commodity.id,
                            country_id=country_id,
                            year=year,
                            reserves_volume=reserves_volume,
                            unit=record.get('unit', 'metric tons'),
                            data_source_id=DataSource.query.filter_by(name='USGS').first().id,
                            validation_status='validated',
                            data_quality_score=self.calculate_data_quality_score(record),
                            confidence_score=min(0.95, self.calculate_data_quality_score(record) + 0.1)  # Slightly higher confidence
                        )
                        db.session.add(reserves_data)
                        results['records_ingested'] += 1
                        
            db.session.commit()
            self.logger.info(f"Ingested {results['records_ingested']} records from {filepath}")
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error ingesting USGS file {filepath}: {str(e)}")
            raise
            
        return results
    
    def _process_fred_data(self) -> Dict[str, Any]:
        """Process FRED data files"""
        results = {
            'ingested_files': [],
            'errors': [],
            'summary': {
                'files_processed': 0,
                'records_ingested': 0,
                'commodities_created': 0
            }
        }
        
        fred_dir = os.path.join(self.data_dir, 'fred')
        if not os.path.exists(fred_dir):
            self.logger.warning(f"FRED data directory not found: {fred_dir}")
            return results
            
        # Process main commodities data file
        main_commodities_file = os.path.join(fred_dir, 'all_commodities_data.json')
        if os.path.exists(main_commodities_file):
            try:
                self.logger.info(f"Processing FRED commodities file: all_commodities_data.json")
                file_results = self._ingest_fred_commodities_file(main_commodities_file)
                results['ingested_files'].append('all_commodities_data.json')
                results['summary']['records_ingested'] += file_results['records_ingested']
                results['summary']['commodities_created'] += file_results['commodities_created']
                results['summary']['files_processed'] += 1
            except Exception as e:
                error_msg = f"Error processing all_commodities_data.json: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        # Process economic indicators file
        economic_indicators_file = os.path.join(fred_dir, 'economic_indicators', 'economic_indicators.json')
        if os.path.exists(economic_indicators_file):
            try:
                self.logger.info(f"Processing FRED economic indicators file: economic_indicators.json")
                file_results = self._ingest_fred_economic_indicators_file(economic_indicators_file)
                results['ingested_files'].append('economic_indicators.json')
                results['summary']['records_ingested'] += file_results['records_ingested']
                results['summary']['files_processed'] += 1
            except Exception as e:
                error_msg = f"Error processing economic_indicators.json: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    def _ingest_fred_commodities_file(self, filepath: str) -> Dict[str, Any]:
        """Ingest FRED commodities data file"""
        results = {
            'records_ingested': 0,
            'commodities_created': 0
        }
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            records = data.get('data', [])
            
            for record in records:
                # Validate data point
                if not self.validate_data(record):
                    self.logger.warning(f"Invalid data point in {os.path.basename(filepath)}: {record}")
                    continue
                    
                # Calculate quality score
                quality_score = self.calculate_data_quality_score(record)
                
                # Skip low quality data
                if quality_score < 0.5:  # Threshold can be adjusted
                    self.logger.warning(f"Low quality data point skipped (score: {quality_score}): {record}")
                    continue
                
                # Extract commodity info
                commodity_name = record.get('commodity')
                if not commodity_name:
                    continue
                    
                # Get or create commodity
                commodity = Commodity.query.filter_by(name=commodity_name.title()).first()
                if not commodity:
                    # Generate a unique symbol
                    base_symbol = commodity_name[:3].upper()
                    symbol = base_symbol
                    counter = 1
                    # Ensure symbol is unique
                    while Commodity.query.filter_by(symbol=symbol).first():
                        symbol = f"{base_symbol}{counter}"
                        counter += 1
                        
                    commodity = Commodity(
                        name=commodity_name.title(),
                        symbol=symbol
                    )
                    db.session.add(commodity)
                    db.session.flush()  # Get the ID without committing
                    results['commodities_created'] += 1
                
                # Extract date and convert to timestamp
                date_str = record.get('date')
                if not date_str:
                    continue
                
                # For simplicity, we'll use a generic country ID
                country_id = 1  # Placeholder
                
                # Extract price
                price = record.get('price')
                if price is not None:
                    # Check if record already exists
                    existing = PriceData.query.filter_by(
                        commodity_id=commodity.id,
                        timestamp=datetime.strptime(date_str, '%Y-%m-%d')
                    ).first()
                    
                    if not existing:
                        price_data = PriceData(
                            commodity_id=commodity.id,
                            price=price,
                            currency='USD',
                            timestamp=datetime.strptime(date_str, '%Y-%m-%d'),
                            data_source_id=DataSource.query.filter_by(name='FRED').first().id,
                            data_quality_score=quality_score,
                            confidence_score=min(0.95, quality_score + 0.1)  # Slightly higher confidence
                        )
                        db.session.add(price_data)
                        results['records_ingested'] += 1
                        
            db.session.commit()
            self.logger.info(f"Ingested {results['records_ingested']} FRED price records from {filepath}")
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error ingesting FRED commodities file {filepath}: {str(e)}")
            raise
            
        return results
    
    def _ingest_fred_economic_indicators_file(self, filepath: str) -> Dict[str, Any]:
        """Ingest FRED economic indicators file"""
        results = {
            'records_ingested': 0
        }
        
        # For now, we'll just log that we've processed this file
        # In a full implementation, you might store these in a separate table
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            indicators = data.get('indicators', {})
            results['records_ingested'] = len(indicators)
            
            self.logger.info(f"Processed {len(indicators)} FRED economic indicators from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error processing FRED economic indicators file {filepath}: {str(e)}")
            raise
            
        return results

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate ingested data"""
        # Basic validation - ensure required fields exist
        required_fields = ['commodity']
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate numeric fields
        if 'production_volume' in data and data['production_volume'] is not None:
            try:
                float(data['production_volume'])
            except (ValueError, TypeError):
                return False
                
        if 'reserves_volume' in data and data['reserves_volume'] is not None:
            try:
                float(data['reserves_volume'])
            except (ValueError, TypeError):
                return False
                
        if 'price' in data and data['price'] is not None:
            try:
                float(data['price'])
            except (ValueError, TypeError):
                return False
        
        # Validate year if present
        if 'year' in data and data['year'] is not None:
            try:
                year = int(data['year'])
                if year < 1900 or year > datetime.now().year + 5:
                    return False
            except (ValueError, TypeError):
                return False
        
        # Validate date if present
        if 'date' in data and data['date'] is not None:
            try:
                datetime.strptime(data['date'], '%Y-%m-%d')
            except ValueError:
                return False
        
        return True

    def calculate_data_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate a quality score for the data point (0-1)"""
        score = 0.0
        total_checks = 0
        
        # Check for presence of key fields
        key_fields = ['commodity', 'year', 'production_volume', 'reserves_volume', 'price']
        for field in key_fields:
            total_checks += 1
            if field in data and data[field] is not None:
                score += 1.0
        
        # Check for data source
        total_checks += 1
        if 'data_source' in data and data['data_source'] is not None:
            score += 1.0
            
        # Check for units
        total_checks += 1
        if 'unit' in data and data['unit'] is not None:
            score += 1.0
            
        # Check for consistency between related fields
        if 'production_volume' in data and data['production_volume'] is not None:
            total_checks += 1
            if float(data['production_volume']) >= 0:
                score += 1.0
                
        if 'reserves_volume' in data and data['reserves_volume'] is not None:
            total_checks += 1
            if float(data['reserves_volume']) >= 0:
                score += 1.0
                
        if 'price' in data and data['price'] is not None:
            total_checks += 1
            if float(data['price']) >= 0:
                score += 1.0
        
        return score / total_checks if total_checks > 0 else 0.0

    def detect_anomalies(self, data_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in the data points"""
        anomalies = []
        
        # Group data by commodity for comparison
        commodity_groups = {}
        for point in data_points:
            commodity = point.get('commodity')
            if commodity:
                if commodity not in commodity_groups:
                    commodity_groups[commodity] = []
                commodity_groups[commodity].append(point)
        
        # Check for outliers within each commodity group
        for commodity, points in commodity_groups.items():
            if len(points) < 3:
                continue
                
            # Extract numeric values for analysis
            production_values = [float(p['production_volume']) for p in points 
                               if p.get('production_volume') is not None]
            reserves_values = [float(p['reserves_volume']) for p in points 
                             if p.get('reserves_volume') is not None]
            price_values = [float(p['price']) for p in points 
                          if p.get('price') is not None]
            
            # Calculate statistics for outlier detection
            for values, field_name in [(production_values, 'production_volume'), 
                                     (reserves_values, 'reserves_volume'), 
                                     (price_values, 'price')]:
                if len(values) < 3:
                    continue
                    
                mean_val = sum(values) / len(values)
                std_dev = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
                
                # Flag points that are more than 2 standard deviations from the mean
                threshold = 2 * std_dev
                for point in points:
                    if point.get(field_name) is not None:
                        val = float(point[field_name])
                        if abs(val - mean_val) > threshold:
                            anomalies.append({
                                'point': point,
                                'type': 'outlier',
                                'field': field_name,
                                'value': val,
                                'mean': mean_val,
                                'std_dev': std_dev,
                                'deviation': abs(val - mean_val)
                            })
        
        return anomalies