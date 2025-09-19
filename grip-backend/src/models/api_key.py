from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from src.models.user import db

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String(100), nullable=False, unique=True)
    api_key = Column(Text, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<APIKey {self.service_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Don't expose the actual API key in responses
            'has_key': bool(self.api_key)
        }
    
    @classmethod
    def get_key(cls, service_name):
        """Get API key for a service"""
        api_key = cls.query.filter_by(service_name=service_name, is_active=True).first()
        return api_key.api_key if api_key else None
    
    @classmethod
    def set_key(cls, service_name, api_key, description=None):
        """Set or update API key for a service"""
        existing = cls.query.filter_by(service_name=service_name).first()
        if existing:
            existing.api_key = api_key
            existing.description = description
            existing.is_active = True
            existing.updated_at = func.now()
        else:
            new_key = cls(
                service_name=service_name,
                api_key=api_key,
                description=description
            )
            db.session.add(new_key)
        
        db.session.commit()
        return True

