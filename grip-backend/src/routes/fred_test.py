from flask import Blueprint, request, jsonify
from src.data_collectors.fred_collector import FREDCollector

fred_test_bp = Blueprint('fred_test', __name__)

@fred_test_bp.route('/api/fred/test', methods=['GET'])
def test_fred_connection():
    """Test FRED API connection"""
    try:
        collector = FREDCollector()
        result = collector.test_connection()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@fred_test_bp.route('/api/fred/commodities', methods=['GET'])
def get_fred_commodities():
    """Get available FRED commodities"""
    try:
        collector = FREDCollector()
        commodities = list(collector.commodity_series.keys())
        return jsonify({
            'success': True,
            'commodities': commodities,
            'count': len(commodities)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@fred_test_bp.route('/api/fred/collect/<commodity>', methods=['GET'])
def collect_fred_data(commodity):
    """Collect FRED data for a specific commodity"""
    try:
        collector = FREDCollector()
        
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        result = collector.collect_price_data(
            commodity_name=commodity,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@fred_test_bp.route('/api/fred/search/<commodity>', methods=['GET'])
def search_fred_series(commodity):
    """Search for FRED series related to a commodity"""
    try:
        collector = FREDCollector()
        result = collector.search_commodity_series(commodity)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@fred_test_bp.route('/api/fred/indicators', methods=['GET'])
def get_economic_indicators():
    """Get economic indicators from FRED"""
    try:
        collector = FREDCollector()
        result = collector.get_economic_indicators()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

