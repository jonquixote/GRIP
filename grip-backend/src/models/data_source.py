from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class DataSource(db.Model):
    __tablename__ = 'data_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.Text)
    api_endpoint = db.Column(db.Text)
    update_frequency = db.Column(db.String(50))
    reliability_score = db.Column(db.Numeric(3, 2))
    last_updated = db.Column(db.DateTime)
    # Enhanced metadata fields
    data_quality_score = db.Column(db.Numeric(3, 2))  # Overall quality score (0-1)
    geographic_coverage = db.Column(db.Text)  # JSON list of covered countries/regions
    temporal_coverage_start = db.Column(db.Date)  # Start date of available data
    temporal_coverage_end = db.Column(db.Date)  # End date of available data
    data_format = db.Column(db.String(50))  # JSON, CSV, API, PDF, etc.
    licensing_terms = db.Column(db.Text)  # Description of usage rights
    contact_info = db.Column(db.Text)  # Contact information for data source
    verification_method = db.Column(db.String(100))  # How data is verified
    data_refresh_rate = db.Column(db.String(50))  # How often data is refreshed
    data_latency = db.Column(db.Integer)  # Latency in days between event and data availability
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    production_data = db.relationship('ProductionData', backref='data_source', lazy=True)
    reserves_data = db.relationship('ReservesData', backref='data_source', lazy=True)
    price_data = db.relationship('PriceData', backref='data_source', lazy=True)

    def __repr__(self):
        return f'<DataSource {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'api_endpoint': self.api_endpoint,
            'update_frequency': self.update_frequency,
            'reliability_score': float(self.reliability_score) if self.reliability_score else None,
            'data_quality_score': float(self.data_quality_score) if self.data_quality_score else None,
            'geographic_coverage': self.geographic_coverage,
            'temporal_coverage_start': self.temporal_coverage_start.isoformat() if self.temporal_coverage_start else None,
            'temporal_coverage_end': self.temporal_coverage_end.isoformat() if self.temporal_coverage_end else None,
            'data_format': self.data_format,
            'licensing_terms': self.licensing_terms,
            'contact_info': self.contact_info,
            'verification_method': self.verification_method,
            'data_refresh_rate': self.data_refresh_rate,
            'data_latency': self.data_latency,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

