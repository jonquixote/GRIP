from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.production_data import ProductionData
from src.models.reserves_data import ReservesData
from src.models.price_data import PriceData
from src.models.data_source import DataSource
from src.models.commodity import Commodity
from sqlalchemy import and_, func, case
from datetime import datetime

data_bp = Blueprint('data', __name__)

# Production Data Routes
@data_bp.route('/production', methods=['GET'])
def get_production_data():
    """Get production data with optional filtering"""
    try:
        commodity_id = request.args.get('commodity_id', type=int)
        country_id = request.args.get('country_id', type=int)
        year = request.args.get('year', type=int)
        
        query = ProductionData.query
        
        if commodity_id:
            query = query.filter(ProductionData.commodity_id == commodity_id)
        if country_id:
            query = query.filter(ProductionData.country_id == country_id)
        if year:
            query = query.filter(ProductionData.year == year)
            
        production_data = query.all()
        return jsonify([data.to_dict() for data in production_data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/production', methods=['POST'])
def create_production_data():
    """Create new production data"""
    try:
        data = request.get_json()
        
        production_data = ProductionData(
            commodity_id=data.get('commodity_id'),
            country_id=data.get('country_id'),
            year=data.get('year'),
            production_volume=data.get('production_volume'),
            unit=data.get('unit'),
            data_source_id=data.get('data_source_id'),
            validation_status=data.get('validation_status', 'pending')
        )
        
        db.session.add(production_data)
        db.session.commit()
        
        return jsonify(production_data.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Reserves Data Routes
@data_bp.route('/reserves', methods=['GET'])
def get_reserves_data():
    """Get reserves data with optional filtering"""
    try:
        commodity_id = request.args.get('commodity_id', type=int)
        country_id = request.args.get('country_id', type=int)
        year = request.args.get('year', type=int)
        
        query = ReservesData.query
        
        if commodity_id:
            query = query.filter(ReservesData.commodity_id == commodity_id)
        if country_id:
            query = query.filter(ReservesData.country_id == country_id)
        if year:
            query = query.filter(ReservesData.year == year)
            
        reserves_data = query.all()
        return jsonify([data.to_dict() for data in reserves_data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/reserves', methods=['POST'])
def create_reserves_data():
    """Create new reserves data"""
    try:
        data = request.get_json()
        
        reserves_data = ReservesData(
            commodity_id=data.get('commodity_id'),
            country_id=data.get('country_id'),
            year=data.get('year'),
            reserves_volume=data.get('reserves_volume'),
            unit=data.get('unit'),
            data_source_id=data.get('data_source_id'),
            validation_status=data.get('validation_status', 'pending')
        )
        
        db.session.add(reserves_data)
        db.session.commit()
        
        return jsonify(reserves_data.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Price Data Routes
@data_bp.route('/prices', methods=['GET'])
def get_price_data():
    """Get price data with optional filtering"""
    try:
        commodity_id = request.args.get('commodity_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        
        query = PriceData.query
        
        if commodity_id:
            query = query.filter(PriceData.commodity_id == commodity_id)
            
        price_data = query.order_by(PriceData.timestamp.desc()).limit(limit).all()
        return jsonify([data.to_dict() for data in price_data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/prices', methods=['POST'])
def create_price_data():
    """Create new price data"""
    try:
        data = request.get_json()
        
        price_data = PriceData(
            commodity_id=data.get('commodity_id'),
            price=data.get('price'),
            currency=data.get('currency', 'USD'),
            exchange=data.get('exchange'),
            timestamp=data.get('timestamp'),
            volume=data.get('volume'),
            data_source_id=data.get('data_source_id')
        )
        
        db.session.add(price_data)
        db.session.commit()
        
        return jsonify(price_data.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Data Sources Routes
@data_bp.route('/data-sources', methods=['GET'])
def get_data_sources():
    """Get all data sources"""
    try:
        data_sources = DataSource.query.all()
        return jsonify([source.to_dict() for source in data_sources])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/data-sources', methods=['POST'])
def create_data_source():
    """Create a new data source"""
    try:
        data = request.get_json()
        
        data_source = DataSource(
            name=data.get('name'),
            url=data.get('url'),
            api_endpoint=data.get('api_endpoint'),
            update_frequency=data.get('update_frequency'),
            reliability_score=data.get('reliability_score'),
            data_quality_score=data.get('data_quality_score'),
            geographic_coverage=data.get('geographic_coverage'),
            temporal_coverage_start=datetime.strptime(data.get('temporal_coverage_start'), '%Y-%m-%d') if data.get('temporal_coverage_start') else None,
            temporal_coverage_end=datetime.strptime(data.get('temporal_coverage_end'), '%Y-%m-%d') if data.get('temporal_coverage_end') else None,
            data_format=data.get('data_format'),
            licensing_terms=data.get('licensing_terms'),
            contact_info=data.get('contact_info'),
            verification_method=data.get('verification_method'),
            data_refresh_rate=data.get('data_refresh_rate'),
            data_latency=data.get('data_latency')
        )
        
        db.session.add(data_source)
        db.session.commit()
        
        return jsonify(data_source.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@data_bp.route('/data-sources/<int:source_id>', methods=['GET'])
def get_data_source(source_id):
    """Get a specific data source by ID"""
    try:
        data_source = DataSource.query.get_or_404(source_id)
        return jsonify(data_source.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/data-sources/<int:source_id>/metadata', methods=['GET'])
def get_data_source_metadata(source_id):
    """Get detailed metadata for a specific data source"""
    try:
        data_source = DataSource.query.get_or_404(source_id)
        
        # Get counts of data points from this source
        production_count = ProductionData.query.filter_by(data_source_id=source_id).count()
        reserves_count = ReservesData.query.filter_by(data_source_id=source_id).count()
        price_count = PriceData.query.filter_by(data_source_id=source_id).count()
        
        # Get date range of data
        production_dates = db.session.query(
            func.min(ProductionData.year).label('min_year'),
            func.max(ProductionData.year).label('max_year')
        ).filter(ProductionData.data_source_id == source_id).first()
        
        price_dates = db.session.query(
            func.min(PriceData.timestamp).label('min_date'),
            func.max(PriceData.timestamp).label('max_date')
        ).filter(PriceData.data_source_id == source_id).first()
        
        # Get quality metrics
        avg_quality = db.session.query(
            func.avg(ProductionData.data_quality_score).label('avg_quality')
        ).filter(ProductionData.data_source_id == source_id).first()
        
        return jsonify({
            'source': data_source.to_dict(),
            'data_counts': {
                'production_records': production_count,
                'reserves_records': reserves_count,
                'price_records': price_count,
                'total_records': production_count + reserves_count + price_count
            },
            'temporal_coverage': {
                'production_years': {
                    'min': production_dates.min_year,
                    'max': production_dates.max_year
                } if production_dates else None,
                'price_dates': {
                    'min': price_dates.min_date.isoformat() if price_dates and price_dates.min_date else None,
                    'max': price_dates.max_date.isoformat() if price_dates and price_dates.max_date else None
                } if price_dates else None
            },
            'quality_metrics': {
                'average_data_quality': float(avg_quality.avg_quality) if avg_quality and avg_quality.avg_quality else None
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Data Quality Routes
@data_bp.route('/data-quality', methods=['GET'])
def get_data_quality_metrics():
    """Get data quality metrics for all commodities"""
    try:
        # Get quality metrics for production data
        production_quality = db.session.query(
            func.avg(ProductionData.data_quality_score).label('avg_quality'),
            func.count(ProductionData.id).label('total_records'),
            func.sum(case((ProductionData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).first()
        
        # Get quality metrics for reserves data
        reserves_quality = db.session.query(
            func.avg(ReservesData.data_quality_score).label('avg_quality'),
            func.count(ReservesData.id).label('total_records'),
            func.sum(case((ReservesData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).first()
        
        # Get quality metrics for price data
        price_quality = db.session.query(
            func.avg(PriceData.data_quality_score).label('avg_quality'),
            func.count(PriceData.id).label('total_records'),
            func.sum(case((PriceData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).first()
        
        # Calculate overall metrics
        total_records = (production_quality.total_records or 0) + \
                         (reserves_quality.total_records or 0) + \
                         (price_quality.total_records or 0)
                         
        high_quality_records = (production_quality.high_quality_count or 0) + \
                              (reserves_quality.high_quality_count or 0) + \
                              (price_quality.high_quality_count or 0)
                              
        overall_quality = (high_quality_records / total_records * 100) if total_records > 0 else 0
        
        return jsonify({
            'overall_quality_score': round(overall_quality, 2),
            'total_records': total_records,
            'high_quality_records': high_quality_records,
            'breakdown': {
                'production': {
                    'avg_quality_score': round(float(production_quality.avg_quality or 0), 2),
                    'total_records': production_quality.total_records or 0,
                    'high_quality_records': production_quality.high_quality_count or 0
                },
                'reserves': {
                    'avg_quality_score': round(float(reserves_quality.avg_quality or 0), 2),
                    'total_records': reserves_quality.total_records or 0,
                    'high_quality_records': reserves_quality.high_quality_count or 0
                },
                'price': {
                    'avg_quality_score': round(float(price_quality.avg_quality or 0), 2),
                    'total_records': price_quality.total_records or 0,
                    'high_quality_records': price_quality.high_quality_count or 0
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/data-quality/<int:commodity_id>', methods=['GET'])
def get_commodity_data_quality(commodity_id):
    """Get data quality metrics for a specific commodity"""
    try:
        # Get quality metrics for production data
        production_quality = db.session.query(
            func.avg(ProductionData.data_quality_score).label('avg_quality'),
            func.count(ProductionData.id).label('total_records'),
            func.sum(case((ProductionData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).filter(ProductionData.commodity_id == commodity_id).first()
        
        # Get quality metrics for reserves data
        reserves_quality = db.session.query(
            func.avg(ReservesData.data_quality_score).label('avg_quality'),
            func.count(ReservesData.id).label('total_records'),
            func.sum(case((ReservesData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).filter(ReservesData.commodity_id == commodity_id).first()
        
        # Get quality metrics for price data
        price_quality = db.session.query(
            func.avg(PriceData.data_quality_score).label('avg_quality'),
            func.count(PriceData.id).label('total_records'),
            func.sum(case((PriceData.data_quality_score >= 0.8, 1), else_=0)).label('high_quality_count')
        ).filter(PriceData.commodity_id == commodity_id).first()
        
        # Get commodity name
        commodity = Commodity.query.get(commodity_id)
        if not commodity:
            return jsonify({'error': 'Commodity not found'}), 404
        
        # Calculate overall metrics
        total_records = (production_quality.total_records or 0) + \
                         (reserves_quality.total_records or 0) + \
                         (price_quality.total_records or 0)
                         
        high_quality_records = (production_quality.high_quality_count or 0) + \
                              (reserves_quality.high_quality_count or 0) + \
                              (price_quality.high_quality_count or 0)
                              
        overall_quality = (high_quality_records / total_records * 100) if total_records > 0 else 0
        
        return jsonify({
            'commodity': commodity.to_dict(),
            'overall_quality_score': round(overall_quality, 2),
            'total_records': total_records,
            'high_quality_records': high_quality_records,
            'breakdown': {
                'production': {
                    'avg_quality_score': round(float(production_quality.avg_quality or 0), 2),
                    'total_records': production_quality.total_records or 0,
                    'high_quality_records': production_quality.high_quality_count or 0
                },
                'reserves': {
                    'avg_quality_score': round(float(reserves_quality.avg_quality or 0), 2),
                    'total_records': reserves_quality.total_records or 0,
                    'high_quality_records': reserves_quality.high_quality_count or 0
                },
                'price': {
                    'avg_quality_score': round(float(price_quality.avg_quality or 0), 2),
                    'total_records': price_quality.total_records or 0,
                    'high_quality_records': price_quality.high_quality_count or 0
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500