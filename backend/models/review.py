from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, and_, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .dbconfig import db




class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    # Serialization rules
    serializer_rules= ['review_id', 'client_id', 'rating', 'comment', 'date_submitted']
       
    review_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    date_submitted = db.Column(db.Date, nullable=False)
    
    
    __table_args__ = (db.CheckConstraint(and_(comment != '', comment.isnot(None)), name='check_comment_not_empty'),)
    
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_validity'),
    )

    client = db.relationship("User", backref="reviews")
    
    def __repr__(self):
        return f'Review({self.review_id}, {self.rating}/5)'