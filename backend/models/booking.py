from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db



class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

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