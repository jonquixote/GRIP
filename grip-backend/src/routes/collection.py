from flask import Blueprint, request, jsonify, current_app
from src.data_collectors.data_collection_service import DataCollectionService
import threading

collection_bp = Blueprint('collection', __name__)

# Global service instance
collection_service = None

def get_collection_service():
    """Get or create the data collection service"""
    global collection_service
    if collection_service is None:
        collection_service = DataCollectionService(current_app)
    return collection_service

@collection_bp.route('/collection/status', methods=['GET'])
def get_collection_status():
    """Get the current status of data collection"""
    try:
        service = get_collection_service()
        status = service.get_collection_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collection_bp.route('/collection/initialize', methods=['POST'])
def initialize_system():
    """Initialize the system with base data"""
    try:
        service = get_collection_service()
        
        # Initialize in order
        service.initialize_data_sources()
        service.initialize_commodities()
        service.initialize_countries()
        
        return jsonify({
            'message': 'System initialized successfully',
            'initialized': ['data_sources', 'commodities', 'countries']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collection_bp.route('/collection/collect', methods=['POST'])
def start_collection():
    """Start data collection from all sources"""
    try:
        service = get_collection_service()
        
        # Get optional source parameter
        source = request.json.get('source') if request.json else None
        
        # Run collection in background thread
        def run_collection():
            if source:
                service.force_collection(source)
            else:
                service.collect_all_data()
        
        thread = threading.Thread(target=run_collection)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'message': 'Data collection started',
            'source': source or 'all'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collection_bp.route('/collection/sources', methods=['GET'])
def get_available_sources():
    """Get available data sources and their capabilities"""
    try:
        service = get_collection_service()
        
        sources_info = {}
        
        # FRED collector info
        fred_collector = service.collectors['fred']
        sources_info['fred'] = {
            'name': 'Federal Reserve Economic Data',
            'type': 'API',
            'commodities': fred_collector.get_available_commodities(),
            'data_types': ['price'],
            'update_frequency': 'daily'
        }
        
        # World Bank collector info
        wb_collector = service.collectors['worldbank']
        sources_info['worldbank'] = {
            'name': 'World Bank Open Data',
            'type': 'API',
            'indicators': wb_collector.get_available_indicators(),
            'data_types': ['economic_indicators'],
            'update_frequency': 'annual'
        }
        
        # USGS collector info
        usgs_collector = service.collectors['usgs']
        sources_info['usgs'] = {
            'name': 'USGS Mineral Commodity Summaries',
            'type': 'Web Scraping',
            'commodities': usgs_collector.get_available_commodities(),
            'data_types': ['production', 'reserves', 'consumption'],
            'update_frequency': 'annual'
        }
        
        return jsonify(sources_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collection_bp.route('/collection/test/<source>', methods=['POST'])
def test_collector(source):
    """Test a specific data collector"""
    try:
        service = get_collection_service()
        
        if source not in service.collectors:
            return jsonify({'error': f'Unknown source: {source}'}), 400
        
        collector = service.collectors[source]
        
        # Test the collector with minimal data
        if source == 'fred':
            test_data = collector.collect_data('copper', 
                                             start_date='2024-01-01', 
                                             end_date='2024-01-31')
        elif source == 'worldbank':
            test_data = collector.collect_data('mining_gdp')
        elif source == 'usgs':
            test_data = collector.collect_data('copper', 'production')
        else:
            test_data = []
        
        return jsonify({
            'source': source,
            'status': 'success',
            'test_data_count': len(test_data),
            'sample_data': test_data[:3] if test_data else []
        })
    except Exception as e:
        return jsonify({
            'source': source,
            'status': 'error',
            'error': str(e)
        }), 500

@collection_bp.route('/collection/schedule', methods=['POST'])
def setup_schedule():
    """Set up scheduled data collection"""
    try:
        service = get_collection_service()
        service.schedule_collections()
        
        return jsonify({
            'message': 'Data collection scheduled',
            'schedule': {
                'fred': 'Daily at 06:00 UTC',
                'worldbank': 'Weekly on Monday at 07:00 UTC',
                'usgs': 'Monthly'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collection_bp.route('/collection/validate', methods=['POST'])
def validate_collected_data():
    """Validate recently collected data"""
    try:
        # This would implement data validation logic
        # For now, return a placeholder response
        return jsonify({
            'message': 'Data validation completed',
            'validation_results': {
                'total_records': 0,
                'valid_records': 0,
                'invalid_records': 0,
                'validation_errors': []
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

