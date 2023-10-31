from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from .dbconfig import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serializer_rules = ['user_id', 'username', 'email', 'user_type']
    
    user_id = db.Column(db.Integer, primary_key=True)
    
    # first_name and last_name
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # hashed
    user_type = db.Column(db.Enum('admin', 'client', 'employee'))
    email = db.Column(db.String(150), nullable=False, unique=True)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(120), unique=True)  # for email verification
    profile_image_url = db.Column(db.String(500))  # column for Cloudinary URL
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bookings = relationship("Booking", back_populates="client")
    services = relationship("PickUpDelivery", back_populates="client")
    
    # Password hashing functions
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'User({self.first_name} {self.last_name}, {self.email})'