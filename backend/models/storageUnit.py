from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db


class StorageUnit(db.Model, SerializerMixin):
    __tablename__ = 'storage_units'
    serializer_rules = ['unit_id', 'size', 'price', 'availability_status']
    
    unit_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability_status = db.Column(db.Enum('available', 'booked', 'under maintenance'), nullable=False)

    
    
    booking = relationship("Booking", uselist=False, back_populates="unit")
    
    # Explicit CheckConstraint 
    __table_args__ = (db.CheckConstraint(price >= 0, name='check_price_positive'),)
    
    def __repr__(self):
        return f'StorageUnit({self.unit_id}, {self.size})'