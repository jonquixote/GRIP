from flask import Blueprint, request, jsonify
from src.models.api_key import APIKey
from src.models.user import db

api_keys_bp = Blueprint('api_keys', __name__)

@api_keys_bp.route('/api/api-keys', methods=['GET'])
def get_api_keys():
    """Get all configured API keys (without exposing actual keys)"""
    try:
        api_keys = APIKey.query.all()
        return jsonify([key.to_dict() for key in api_keys])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_keys_bp.route('/api/api-keys', methods=['POST'])
def create_or_update_api_key():
    """Create or update an API key"""
    try:
        data = request.get_json()
        
        if not data or 'service_name' not in data or 'api_key' not in data:
            return jsonify({'error': 'service_name and api_key are required'}), 400
        
        service_name = data['service_name']
        api_key = data['api_key']
        description = data.get('description', '')
        
        # Validate service name
        valid_services = ['fred', 'world_bank', 'usgs', 'quandl', 'alpha_vantage', 'iex_cloud']
        if service_name not in valid_services:
            return jsonify({'error': f'Invalid service name. Must be one of: {valid_services}'}), 400
        
        APIKey.set_key(service_name, api_key, description)
        
        return jsonify({'message': f'API key for {service_name} updated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_keys_bp.route('/api/api-keys/<service_name>', methods=['DELETE'])
def delete_api_key(service_name):
    """Deactivate an API key"""
    try:
        api_key = APIKey.query.filter_by(service_name=service_name).first()
        if not api_key:
            return jsonify({'error': 'API key not found'}), 404
        
        api_key.is_active = False
        db.session.commit()
        
        return jsonify({'message': f'API key for {service_name} deactivated'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_keys_bp.route('/api/api-keys/test/<service_name>', methods=['POST'])
def test_api_key(service_name):
    """Test an API key"""
    try:
        api_key = APIKey.get_key(service_name)
        if not api_key:
            return jsonify({'error': f'No API key found for {service_name}'}), 404
        
        # Import the appropriate collector and test
        if service_name == 'fred':
            from src.data_collectors.fred_collector import FREDCollector
            collector = FREDCollector()
            result = collector.test_connection()
        elif service_name == 'world_bank':
            from src.data_collectors.worldbank_collector import WorldBankCollector
            collector = WorldBankCollector()
            result = collector.test_connection()
        elif service_name == 'usgs':
            from src.data_collectors.usgs_collector import USGSCollector
            collector = USGSCollector()
            result = collector.test_connection()
        else:
            return jsonify({'error': f'Testing not implemented for {service_name}'}), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_keys_bp.route('/api/api-keys/initialize', methods=['POST'])
def initialize_default_keys():
    """Initialize with default API keys for testing"""
    try:
        # Set the provided FRED API key
        APIKey.set_key('fred', '95f42f356f5131f13257eac54897e96a', 'FRED API for economic data')
        
        # World Bank typically doesn't require API key
        APIKey.set_key('world_bank', 'no_key_required', 'World Bank Open Data API')
        
        # USGS doesn't require API key for most data
        APIKey.set_key('usgs', 'no_key_required', 'USGS Mineral Resources Data')
        
        return jsonify({'message': 'Default API keys initialized successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

