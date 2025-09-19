from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.commodity import Commodity

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

