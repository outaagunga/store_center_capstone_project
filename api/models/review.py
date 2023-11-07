from datetime import datetime
from models.database import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # Allowing comments to be optional
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='reviews')
    order = db.relationship('Order', back_populates='reviews')

    def __init__(self, user_id, order_id, rating, comment=None):
        self.user_id = user_id
        self.order_id = order_id
        self.rating = rating
        self.comment = comment

    def __str__(self):
        return f"Review #{self.id} by User #{self.user_id} for Order #{self.order_id}: Rating {self.rating}"
