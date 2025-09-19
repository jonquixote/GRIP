from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    iso_code = db.Column(db.String(3), unique=True)
    continent = db.Column(db.String(50))
    coordinates = db.Column(db.Text)  # Store as JSON string for lat/lng
    political_stability_score = db.Column(db.Numeric(3, 2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    production_data = db.relationship('ProductionData', backref='country', lazy=True)
    reserves_data = db.relationship('ReservesData', backref='country', lazy=True)

    def __repr__(self):
        return f'<Country {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'iso_code': self.iso_code,
            'continent': self.continent,
            'coordinates': self.coordinates,
            'political_stability_score': float(self.political_stability_score) if self.political_stability_score else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

