from flask import Blueprint, request, jsonify, current_app
from src.analytics.analytics_service import AnalyticsService
import threading

analytics_bp = Blueprint('analytics', __name__)

# Global service instance
analytics_service = None

def get_analytics_service():
    """Get or create the analytics service"""
    global analytics_service
    if analytics_service is None:
        analytics_service = AnalyticsService(current_app)
    return analytics_service

@analytics_bp.route('/analytics/commodity/<int:commodity_id>', methods=['GET'])
def analyze_commodity(commodity_id):
    """Analyze a specific commodity"""
    try:
        service = get_analytics_service()
        
        # Get analysis types from query parameters
        analysis_types = request.args.getlist('types')
        if not analysis_types:
            analysis_types = ['price', 'production', 'ml']
        
        result = service.analyze_commodity(commodity_id, analysis_types)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/commodity/<int:commodity_id>/price', methods=['GET'])
def analyze_commodity_price(commodity_id):
    """Analyze commodity price data specifically"""
    try:
        service = get_analytics_service()
        result = service.analyze_commodity(commodity_id, ['price'])
        
        if 'analyses' in result and 'price' in result['analyses']:
            return jsonify(result['analyses']['price'])
        else:
            return jsonify({'error': 'Price analysis not available'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/commodity/<int:commodity_id>/production', methods=['GET'])
def analyze_commodity_production(commodity_id):
    """Analyze commodity production data specifically"""
    try:
        service = get_analytics_service()
        result = service.analyze_commodity(commodity_id, ['production'])
        
        if 'analyses' in result and 'production' in result['analyses']:
            return jsonify(result['analyses']['production'])
        else:
            return jsonify({'error': 'Production analysis not available'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/commodity/<int:commodity_id>/ml', methods=['GET'])
def analyze_commodity_ml(commodity_id):
    """Perform ML analysis on commodity data"""
    try:
        service = get_analytics_service()
        result = service.analyze_commodity(commodity_id, ['ml'])
        
        if 'analyses' in result and 'ml' in result['analyses']:
            return jsonify(result['analyses']['ml'])
        else:
            return jsonify({'error': 'ML analysis not available'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/compare', methods=['POST'])
def compare_commodities():
    """Compare multiple commodities"""
    try:
        service = get_analytics_service()
        data = request.get_json()
        
        if not data or 'commodity_ids' not in data:
            return jsonify({'error': 'commodity_ids required in request body'}), 400
        
        commodity_ids = data['commodity_ids']
        analysis_type = data.get('analysis_type', 'price')
        
        if not isinstance(commodity_ids, list) or len(commodity_ids) < 2:
            return jsonify({'error': 'At least 2 commodity IDs required for comparison'}), 400
        
        result = service.compare_commodities(commodity_ids, analysis_type)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/market-overview', methods=['GET'])
def get_market_overview():
    """Get overall market analysis"""
    try:
        service = get_analytics_service()
        result = service.get_market_overview()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/predict/<int:commodity_id>', methods=['GET'])
def predict_commodity(commodity_id):
    """Get predictions for a commodity"""
    try:
        service = get_analytics_service()
        
        # Get prediction parameters
        periods = request.args.get('periods', 30, type=int)
        
        # Perform ML analysis to get predictions
        result = service.analyze_commodity(commodity_id, ['ml'])
        
        if 'analyses' in result and 'ml' in result['analyses']:
            ml_analysis = result['analyses']['ml']
            predictions = ml_analysis.get('predictions', {})
            
            return jsonify({
                'commodity_id': commodity_id,
                'predictions': predictions,
                'model_performance': ml_analysis.get('model_performance', {}),
                'best_model': ml_analysis.get('best_model', 'unknown'),
                'analysis_date': result.get('analysis_date')
            })
        else:
            return jsonify({'error': 'Prediction analysis not available'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/risk-assessment/<int:commodity_id>', methods=['GET'])
def assess_commodity_risk(commodity_id):
    """Get risk assessment for a commodity"""
    try:
        service = get_analytics_service()
        result = service.analyze_commodity(commodity_id, ['price', 'production'])
        
        risk_assessment = {
            'commodity_id': commodity_id,
            'overall_risk': 'Unknown',
            'risk_factors': [],
            'risk_metrics': {}
        }
        
        # Extract risk information from analyses
        if 'analyses' in result:
            # Price risk
            if 'price' in result['analyses']:
                price_analysis = result['analyses']['price']
                risk_metrics = price_analysis.get('risk_metrics', {})
                risk_assessment['risk_metrics']['price'] = risk_metrics
                
                # Check for high volatility
                volatility = price_analysis.get('volatility', {}).get('daily', 0)
                if volatility > 0.05:
                    risk_assessment['risk_factors'].append('High price volatility')
            
            # Production risk
            if 'production' in result['analyses']:
                production_analysis = result['analyses']['production']
                supply_risk = production_analysis.get('supply_risk', {})
                risk_assessment['risk_metrics']['supply'] = supply_risk
                
                if supply_risk.get('overall_risk') == 'High':
                    risk_assessment['risk_factors'].append('High supply risk')
        
        # Overall risk assessment
        if 'summary' in result:
            risk_assessment['overall_risk'] = result['summary'].get('risk_level', 'Unknown')
        
        return jsonify(risk_assessment)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/trends', methods=['GET'])
def get_market_trends():
    """Get current market trends"""
    try:
        service = get_analytics_service()
        
        # Get trend analysis for multiple commodities
        from src.models.commodity import Commodity
        commodities = Commodity.query.limit(10).all()
        
        trends = {
            'analysis_date': service.analyzers['price'].logger.handlers[0].baseFilename if service.analyzers['price'].logger.handlers else None,
            'trending_up': [],
            'trending_down': [],
            'stable': [],
            'high_volatility': []
        }
        
        for commodity in commodities:
            try:
                analysis = service._perform_analysis(commodity.id, 'price')
                
                if 'error' not in analysis:
                    trend = analysis.get('trend', {}).get('trend', 'stable')
                    volatility = analysis.get('volatility', {}).get('daily', 0)
                    
                    commodity_info = {
                        'id': commodity.id,
                        'name': commodity.name,
                        'trend_strength': analysis.get('trend', {}).get('r_squared', 0)
                    }
                    
                    if trend == 'increasing':
                        trends['trending_up'].append(commodity_info)
                    elif trend == 'decreasing':
                        trends['trending_down'].append(commodity_info)
                    else:
                        trends['stable'].append(commodity_info)
                    
                    if volatility > 0.05:  # 5% daily volatility threshold
                        trends['high_volatility'].append({
                            **commodity_info,
                            'volatility': volatility
                        })
            
            except Exception as e:
                service.logger.error(f"Error analyzing trends for {commodity.name}: {e}")
        
        return jsonify(trends)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/cache', methods=['GET'])
def get_cache_stats():
    """Get analytics cache statistics"""
    try:
        service = get_analytics_service()
        stats = service.get_cache_stats()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/cache', methods=['DELETE'])
def clear_cache():
    """Clear analytics cache"""
    try:
        service = get_analytics_service()
        service.clear_cache()
        return jsonify({'message': 'Analytics cache cleared successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/health', methods=['GET'])
def health_check():
    """Health check for analytics service"""
    try:
        service = get_analytics_service()
        
        health_status = {
            'status': 'healthy',
            'analyzers': {},
            'cache_size': len(service.analysis_cache),
            'timestamp': service.analyzers['price'].logger.handlers[0].baseFilename if service.analyzers['price'].logger.handlers else None
        }
        
        # Check each analyzer
        for analyzer_name, analyzer in service.analyzers.items():
            health_status['analyzers'][analyzer_name] = {
                'name': analyzer.name,
                'status': 'available'
            }
        
        return jsonify(health_status)
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

