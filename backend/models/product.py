from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    serializer_rules = ['product_id', 'name', 'description', 'image_url', 'quantity', 'weight', 'category_id']
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500))  # from Cloudinary
    quantity = db.Column(db.Integer, nullable=False, default=1)
    weight = db.Column(db.Float, nullable=False)  # in kilograms
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    category = relationship("Category", back_populates="products")
    
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'))
    booking = relationship("Booking", back_populates="product")

    def __repr__(self):
        return f'Product({self.name}, Category: {self.category.name})'