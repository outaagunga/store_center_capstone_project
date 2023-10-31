from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db


class PickUpDelivery(db.Model, SerializerMixin):
    __tablename__ = 'pickup_delivery'
    
    # Serialization rules
    serializer_rules = ['service_id', 'client_id', 'service_type', 'date', 'address', 'status']
    
    service_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    service_type = db.Column(db.Enum('pickup', 'delivery'), nullable=False)
    date = db.Column(db.Date,  nullable=False)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('pending', 'on-transit' 'completed'), nullable=False)

    client = relationship("User", back_populates="services")
    
    def __repr__(self):
        return f'PickUpDelivery({self.service_id}, {self.service_type}, {self.status})'