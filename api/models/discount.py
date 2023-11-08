
# from datetime import datetime
# from models.database import db


# class Discount(db.Model):
#     __tablename__ = 'discounts'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(
#         'users.user_id'), nullable=False)
#     order_id = db.Column(db.Integer, db.ForeignKey(
#         'orders.id'), nullable=False)
#     discount_code = db.Column(db.String(20), nullable=False, unique=True)
#     discount_amount = db.Column(db.Float(precision=2), nullable=False)
#     expiration_date = db.Column(db.DateTime, nullable=False)

#     # Relationships
#     user = db.relationship('User', back_populates='discounts')
#     order = db.relationship('Order', back_populates='discounts')

#     def __init__(self, user_id, order_id, discount_code, discount_amount, expiration_date):
#         self.user_id = user_id
#         self.order_id = order_id
#         self.discount_code = discount_code
#         self.discount_amount = discount_amount
#         self.expiration_date = expiration_date

#     def __str__(self):
#         return f"Discount '{self.discount_code}' of ${self.discount_amount} for Order #{self.order_id}"


# class Order(db.Model):
#     __tablename__ = 'orders'

#     id = db.Column(db.Integer, primary_key=True)
#     # ... (Existing fields for Order model)

#     # Relationships
#     discounts = db.relationship('Discount', back_populates='order')

#     # ... (Existing relationships and methods for Order model)
