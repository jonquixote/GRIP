from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.commodity import Commodity
from src.models.production_data import ProductionData
from src.models.reserves_data import ReservesData
from src.models.price_data import PriceData
from sqlalchemy import func, and_

commodity_bp = Blueprint('commodity', __name__)

@commodity_bp.route('/commodities', methods=['GET'])
def get_commodities():
    """Get all commodities"""
    try:
        commodities = Commodity.query.all()
        return jsonify([commodity.to_dict() for commodity in commodities])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@commodity_bp.route('/commodities/<int:commodity_id>', methods=['GET'])
def get_commodity(commodity_id):
    """Get a specific commodity by ID"""
    try:
        commodity = Commodity.query.get_or_404(commodity_id)
        return jsonify(commodity.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@commodity_bp.route('/commodities/<int:commodity_id>/details', methods=['GET'])
def get_commodity_details(commodity_id):
    """Get detailed commodity information including production, reserves, and price data"""
    try:
        commodity = Commodity.query.get_or_404(commodity_id)
        
        # Get recent production data (last 10 years)
        production_data = ProductionData.query.filter_by(commodity_id=commodity_id)\
            .order_by(ProductionData.year.desc())\
            .limit(10).all()
            
        # Get recent reserves data (last 10 years)
        reserves_data = ReservesData.query.filter_by(commodity_id=commodity_id)\
            .order_by(ReservesData.year.desc())\
            .limit(10).all()
            
        # Get recent price data (last 30 records)
        price_data = PriceData.query.filter_by(commodity_id=commodity_id)\
            .order_by(PriceData.timestamp.desc())\
            .limit(30).all()
            
        # Calculate summary statistics
        total_production = db.session.query(func.sum(ProductionData.production_volume))\
            .filter_by(commodity_id=commodity_id).scalar() or 0
            
        avg_price = db.session.query(func.avg(PriceData.price))\
            .filter_by(commodity_id=commodity_id).scalar()
            
        latest_reserves = db.session.query(ReservesData.reserves_volume)\
            .filter_by(commodity_id=commodity_id)\
            .order_by(ReservesData.year.desc())\
            .first()
            
        return jsonify({
            'commodity': commodity.to_dict(),
            'production_data': [p.to_dict() for p in production_data],
            'reserves_data': [r.to_dict() for r in reserves_data],
            'price_data': [p.to_dict() for p in price_data],
            'summary': {
                'total_production': float(total_production),
                'average_price': float(avg_price) if avg_price else None,
                'latest_reserves': float(latest_reserves.reserves_volume) if latest_reserves else None
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@commodity_bp.route('/commodities', methods=['POST'])
def create_commodity():
    """Create a new commodity"""
    try:
        data = request.get_json()
        
        commodity = Commodity(
            name=data.get('name'),
            symbol=data.get('symbol'),
            category=data.get('category'),
            strategic_importance=data.get('strategic_importance')
        )
        
        db.session.add(commodity)
        db.session.commit()
        
        return jsonify(commodity.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@commodity_bp.route('/commodities/<int:commodity_id>', methods=['PUT'])
def update_commodity(commodity_id):
    """Update a commodity"""
    try:
        commodity = Commodity.query.get_or_404(commodity_id)
        data = request.get_json()
        
        commodity.name = data.get('name', commodity.name)
        commodity.symbol = data.get('symbol', commodity.symbol)
        commodity.category = data.get('category', commodity.category)
        commodity.strategic_importance = data.get('strategic_importance', commodity.strategic_importance)
        
        db.session.commit()
        
        return jsonify(commodity.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@commodity_bp.route('/commodities/<int:commodity_id>', methods=['DELETE'])
def delete_commodity(commodity_id):
    """Delete a commodity"""
    try:
        commodity = Commodity.query.get_or_404(commodity_id)
        db.session.delete(commodity)
        db.session.commit()
        
        return jsonify({'message': 'Commodity deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

