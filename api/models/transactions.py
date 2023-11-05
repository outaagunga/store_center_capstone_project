from datetime import datetime
from api.app import db
from api.models.order import Order


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    transaction_code = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='transactions')
    order = db.relationship('Order', back_populates='transactions')

    def __init__(self, user_id, order_id, amount, transaction_code=None):
        self.user_id = user_id
        self.order_id = order_id
        self.amount = amount
        self.transaction_code = transaction_code

    def get_order(self):
        return Order.query.get(self.order_id)

    def __str__(self):
        return f"Transaction of ${self.amount} for Order #{self.order_id}"
