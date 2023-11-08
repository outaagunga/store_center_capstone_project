from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db
import enum


class ProductCategory(enum.Enum):
    Fragile ="CATEGORY_ONE"
    Perishable = "CATEGORY_TWO"
    Bulk = "CATEGORY_THREE"


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    serializer_rules = ['category_id', 'name']
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(ProductCategory), nullable=False, unique=True)
    
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f'Category({self.name.value})'  # using .value to get the string representation of the enum