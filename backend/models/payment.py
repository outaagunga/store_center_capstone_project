from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    serializer_rules = ['payment_id', 'transaction_id', 'amount', 'method', 'status', 'created_at', 'confirmed_at']
    
    payment_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(255), unique=True, nullable=False)  # Unique Transaction ID from payment gateway
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.Enum('MPESA', 'PayPal'), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'failed'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # When the payment was initiated
    confirmed_at = db.Column(db.DateTime)  # When the payment was confirmed
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Linking payment to a client/user
    
    client = relationship('User', back_populates='payments') 

    def __repr__(self):
        return f'Payment({self.method}, {self.amount}, Status: {self.status})'