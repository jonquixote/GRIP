from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.country import Country

country_bp = Blueprint('country', __name__)

@country_bp.route('/countries', methods=['GET'])
def get_countries():
    """Get all countries"""
    try:
        countries = Country.query.all()
        return jsonify([country.to_dict() for country in countries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@country_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    """Get a specific country by ID"""
    try:
        country = Country.query.get_or_404(country_id)
        return jsonify(country.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@country_bp.route('/countries', methods=['POST'])
def create_country():
    """Create a new country"""
    try:
        data = request.get_json()
        
        country = Country(
            name=data.get('name'),
            iso_code=data.get('iso_code'),
            continent=data.get('continent'),
            coordinates=data.get('coordinates'),
            political_stability_score=data.get('political_stability_score')
        )
        
        db.session.add(country)
        db.session.commit()
        
        return jsonify(country.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@country_bp.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    """Update a country"""
    try:
        country = Country.query.get_or_404(country_id)
        data = request.get_json()
        
        country.name = data.get('name', country.name)
        country.iso_code = data.get('iso_code', country.iso_code)
        country.continent = data.get('continent', country.continent)
        country.coordinates = data.get('coordinates', country.coordinates)
        country.political_stability_score = data.get('political_stability_score', country.political_stability_score)
        
        db.session.commit()
        
        return jsonify(country.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@country_bp.route('/countries/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    """Delete a country"""
    try:
        country = Country.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        
        return jsonify({'message': 'Country deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

