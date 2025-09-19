from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Commodity(db.Model):
    __tablename__ = 'commodities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), unique=True)
    category = db.Column(db.String(50))
    strategic_importance = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    production_data = db.relationship('ProductionData', backref='commodity', lazy=True)
    reserves_data = db.relationship('ReservesData', backref='commodity', lazy=True)
    price_data = db.relationship('PriceData', backref='commodity', lazy=True)

    def __repr__(self):
        return f'<Commodity {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'category': self.category,
            'strategic_importance': self.strategic_importance,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

