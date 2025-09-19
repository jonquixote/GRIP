from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class ProductionData(db.Model):
    __tablename__ = 'production_data'
    
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    production_volume = db.Column(db.Numeric(15, 2))
    unit = db.Column(db.String(20))
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'))
    validation_status = db.Column(db.String(20), default='pending')
    # Metadata fields for tracking
    data_quality_score = db.Column(db.Numeric(3, 2))  # Quality score from 0-1
    confidence_score = db.Column(db.Numeric(3, 2))  # Confidence in the data point (0-1)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Composite unique constraint to prevent duplicate entries
    __table_args__ = (db.UniqueConstraint('commodity_id', 'country_id', 'year', 'data_source_id'),)

    def __repr__(self):
        return f'<ProductionData {self.commodity_id}-{self.country_id}-{self.year}>'

    def to_dict(self):
        return {
            'id': self.id,
            'commodity_id': self.commodity_id,
            'country_id': self.country_id,
            'year': self.year,
            'production_volume': float(self.production_volume) if self.production_volume else None,
            'unit': self.unit,
            'data_source_id': self.data_source_id,
            'validation_status': self.validation_status,
            'data_quality_score': float(self.data_quality_score) if self.data_quality_score else None,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

