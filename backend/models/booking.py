from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint
from datetime import timedelta
from .dbconfig import db



class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

     # adding validation and constraints on the start_date and end_date columns to ensure that start_date is always before end_date.
    __table_args__ = (
        CheckConstraint('start_date <= end_date', name='start_date_end_date_check'),
    )

    # Serialization rules
    # serializer_rules = ['booking_id', 'client_id', 'unit_id', 'start_date', 'end_date', 'goods_description']
    serializer_rules = ['booking_id', 'client_id', 'unit_id', 'start_date', 'end_date', 'product_id']

    booking_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    storage_unit_id = db.Column(db.Integer, db.ForeignKey('storage_units.unit_id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    # goods_description = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.product_id'))
   
    
    client = relationship("User", foreign_keys=[client_id], back_populates="bookings")
    employee = relationship("User", foreign_keys=[employee_id], back_populates="assigned_bookings")
    unit = relationship("StorageUnit", back_populates="bookings")
    product = relationship("Product", foreign_keys=[product_id], back_populates="bookings")
    
    def __repr__(self):
        return f'Booking({self.booking_id}, Product: {self.product.name})'
    
    # Calculating Booking Duration
    def booking_duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None