from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db



class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    # Serialization rules
    serializer_rules = ['booking_id', 'client_id', 'unit_id', 'start_date', 'end_date', 'goods_description']

    booking_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('storage_units.unit_id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # can be nullable if not set
    goods_description = db.Column(db.String, nullable=False)
    
    
    unit = relationship("StorageUnit", backref="bookings")
    
    def __repr__(self):
        return f'Booking({self.booking_id}, {self.client_id})'