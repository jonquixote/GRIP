from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class PriceData(db.Model):
    __tablename__ = 'price_data'
    
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.id'), nullable=False)
    price = db.Column(db.Numeric(10, 4))
    currency = db.Column(db.String(3), default='USD')
    exchange = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, nullable=False)
    volume = db.Column(db.Numeric(15, 2))
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'))
    # Metadata fields for tracking
    data_quality_score = db.Column(db.Numeric(3, 2))  # Quality score from 0-1
    confidence_score = db.Column(db.Numeric(3, 2))  # Confidence in the data point (0-1)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<PriceData {self.commodity_id}-{self.timestamp}>'

    def to_dict(self):
        return {
            'id': self.id,
            'commodity_id': self.commodity_id,
            'price': float(self.price) if self.price else None,
            'currency': self.currency,
            'exchange': self.exchange,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'volume': float(self.volume) if self.volume else None,
            'data_source_id': self.data_source_id,
            'data_quality_score': float(self.data_quality_score) if self.data_quality_score else None,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

