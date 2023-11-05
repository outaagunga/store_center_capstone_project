from datetime import datetime
from api.app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    delivery_date = db.Column(db.DateTime, nullable=False)
    order_reference_code = db.Column(db.String(50), nullable=True)
    invoice = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    number_of_items = db.Column(db.Integer, nullable=True)
    order_reference = db.Column(db.String(50), nullable=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    pickup_date_scheduled = db.Column(db.DateTime, nullable=False)
    pickup_date_actual = db.Column(db.DateTime, nullable=False)
    packed = db.Column(db.Boolean, nullable=False, default=True)
    pickup_address = db.Column(db.String(255), nullable=True)
    pickup_status = db.Column(db.String(20), nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship(
        'OrderItem', back_populates='order', cascade="all, delete-orphan")

    def __init__(self, user_id, delivery_date, total_price, payment_status, pickup_status, pickup_address, pickup_date_scheduled, pickup_date_actual, order_reference_code=None, invoice=None, payment_method=None, number_of_items=None, booking_date=None, booking_status='Pending'):
        self.user_id = user_id
        self.delivery_date = delivery_date
        self.order_reference_code = order_reference_code
        self.invoice = invoice
        self.payment_method = payment_method
        self.number_of_items = number_of_items
        self.order_reference = f"ORDER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.booking_date = booking_date if booking_date else datetime.utcnow()
        self.booking_status = booking_status
        self.total_price = total_price
        self.payment_status = payment_status
        self.pickup_date_scheduled = pickup_date_scheduled
        self.pickup_date_actual = pickup_date_actual
        self.pickup_address = pickup_address
        self.pickup_status = pickup_status

    def __str__(self):
        return f"Order {self.order_reference} by {self.user.username}"


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float(precision=2), nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='order_items')

    def __init__(self, order_id, product_name, quantity, unit_price):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product_name} - ${self.total_price():.2f}"
