from datetime import datetime
from models.database import db
from models.review import Review


class Order(db.Model):
    __tablename__ = 'orders'

    ORDER_REFERENCE_PREFIX = "ORDER-"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    delivery_date = db.Column(db.DateTime, nullable=False)
    order_reference_code = db.Column(db.String(50), unique=True)
    invoice = db.Column(db.String(100))
    payment_method = db.Column(db.String(50))
    number_of_items = db.Column(db.Integer)
    booking_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    pickup_date_scheduled = db.Column(db.DateTime, nullable=False)
    pickup_date_actual = db.Column(db.DateTime, nullable=False)
    packed = db.Column(db.Boolean, default=True, nullable=False)
    pickup_address = db.Column(db.String(255))
    pickup_status = db.Column(db.Boolean)

    # New columns for shipment-related fields
    shipment_status = db.Column(db.String(50))
    shipment_tracking_number = db.Column(db.String(50))
    shipment_carrier = db.Column(db.String(50))
    shipment_eta = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='orders')
    reviews = db.relationship('Review', back_populates='order')

    def __init__(self, user_id, delivery_date, total_price, packed,
                 order_reference_code=None, invoice=None, payment_method=None,
                 number_of_items=None, booking_date=None, booking_status='Pending',
                 shipment_status=None, pickup_date_actual=None, pickup_address=None,
                 pickup_status=None, payment_status=None, pickup_date_scheduled=None,
                 shipment_tracking_number=None, shipment_carrier=None, shipment_eta=None):
        self.user_id = user_id
        self.delivery_date = delivery_date
        self.order_reference_code = order_reference_code or self.generate_order_reference()
        self.invoice = invoice or ""  # Use default values or empty string if not provided
        # Use default values or empty string if not provided
        self.payment_method = payment_method or ""
        # Use default value or 0 if not provided
        self.number_of_items = number_of_items or 0
        self.booking_date = booking_date or datetime.utcnow()
        self.booking_status = booking_status
        self.order_date = datetime.utcnow()
        self.total_price = total_price
        self.packed = packed
        # Use default value or False if not provided
        self.pickup_status = pickup_status or False
        self.pickup_date_actual = pickup_date_actual
        # Use default values or "Unpaid" if not provided
        self.payment_status = payment_status or "Unpaid"
        # Use default values or empty string if not provided
        self.shipment_status = shipment_status or ""
        # Use default values or empty string if not provided
        self.pickup_address = pickup_address or ""
        # Use default values or empty string if not provided
        self.shipment_tracking_number = shipment_tracking_number or ""
        # Use default values or empty string if not provided
        self.shipment_carrier = shipment_carrier or ""
        self.shipment_eta = shipment_eta
        self.pickup_date_scheduled = pickup_date_scheduled or datetime.utcnow()

    def generate_order_reference(self):
        return f"{self.ORDER_REFERENCE_PREFIX}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    def format_date(self, date):
        return date.isoformat() if date else None

    def to_dict(self):
        return {
            'id': self.id,
            'order_date': self.format_date(self.order_date),
            'delivery_date': self.format_date(self.delivery_date),
            'total_price': self.total_price,
            'number_of_items': self.number_of_items,
            'invoice': self.invoice,
            'payment_method': self.payment_method,
            'booking_date': self.format_date(self.booking_date),
            'booking_status': self.booking_status,
            'payment_status': self.payment_status,
            'pickup_date_scheduled': self.format_date(self.pickup_date_scheduled),
            'pickup_date_actual': self.format_date(self.pickup_date_actual),
            'order_reference_code': self.order_reference_code,
            'packed': self.packed,
            'shipment_status': self.shipment_status,
            'shipment_tracking_number': self.shipment_tracking_number,
            'shipment_carrier': self.shipment_carrier,
            'order_reference': self.generate_order_reference(),
            'shipment_eta': self.format_date(self.shipment_eta)
        }

    def __str__(self):
        return f"Order {self.order_reference_code} by {self.user.username}"
