from flask import Blueprint, request, jsonify
from src.data_collectors.usgs_collector import USGSCollector

usgs_test_bp = Blueprint('usgs_test', __name__)

@usgs_test_bp.route('/api/usgs/test', methods=['GET'])
def test_usgs_connection():
    """Test USGS website connection"""
    try:
        collector = USGSCollector()
        result = collector.test_connection()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/commodities', methods=['GET'])
def get_usgs_commodities():
    """Get available USGS commodities"""
    try:
        collector = USGSCollector()
        result = collector.get_available_commodities()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/pdf-links', methods=['GET'])
def get_pdf_links():
    """Get USGS Mineral Commodity Summary PDF links"""
    try:
        collector = USGSCollector()
        year = request.args.get('year', type=int)
        result = collector.get_mineral_commodity_summaries_links(year)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/production/<commodity>', methods=['GET'])
def collect_production_data(commodity):
    """Collect USGS production data for a commodity"""
    try:
        collector = USGSCollector()
        year = request.args.get('year', type=int)
        result = collector.collect_production_data(commodity, year)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/reserves/<commodity>', methods=['GET'])
def collect_reserves_data(commodity):
    """Collect USGS reserves data for a commodity"""
    try:
        collector = USGSCollector()
        year = request.args.get('year', type=int)
        result = collector.collect_reserves_data(commodity, year)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/search/<commodity>', methods=['GET'])
def search_mineral_data(commodity):
    """Search for mineral data on USGS website"""
    try:
        collector = USGSCollector()
        data_type = request.args.get('data_type', 'all')
        result = collector.search_mineral_data(commodity, data_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/parse-pdf', methods=['POST'])
def parse_pdf():
    """Parse a USGS PDF document"""
    try:
        data = request.get_json()
        if not data or 'pdf_url' not in data:
            return jsonify({'success': False, 'error': 'pdf_url is required'}), 400
        
        collector = USGSCollector()
        pdf_url = data['pdf_url']
        commodity = data.get('commodity')
        
        result = collector.parse_mineral_commodity_summary_pdf(pdf_url, commodity)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/historical/<commodity>', methods=['GET'])
def collect_historical_data(commodity):
    """Collect USGS historical data for a commodity from 1900 to present"""
    try:
        collector = USGSCollector()
        start_year = request.args.get('start_year', 1900, type=int)
        end_year = request.args.get('end_year', type=int)  # If not provided, will use current year
        
        result = collector.collect_historical_data(commodity, start_year, end_year)
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@usgs_test_bp.route('/api/usgs/historical-all', methods=['POST'])
def collect_all_historical_data():
    """Collect USGS historical data for all commodities from 1900 to present"""
    try:
        collector = USGSCollector()
        data = request.get_json()
        start_year = data.get('start_year', 1900)
        end_year = data.get('end_year')  # If not provided, will use current year
        commodities = data.get('commodities')  # If not provided, will collect all
        
        all_data = []
        if commodities:
            for commodity in commodities:
                result = collector.collect_historical_data(commodity, start_year, end_year)
                all_data.extend(result)
        else:
            # Collect for all commodities
            result = collector.collect_historical_data(None, start_year, end_year)
            all_data.extend(result)
        
        return jsonify({
            'success': True,
            'data': all_data,
            'count': len(all_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

