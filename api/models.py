# models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True,
                             nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Billing Information Fields
    billing_address = db.Column(db.String(255), nullable=True)
    credit_card_number = db.Column(db.String(16), nullable=True)
    credit_card_expiration = db.Column(db.String(5), nullable=True)
    security_code = db.Column(db.String(3), nullable=True)
    paypal_email = db.Column(db.String(100), nullable=True)
    mpesa_phone_number = db.Column(db.String(15), nullable=True)

    def has_billing_info(self):
        """
        Check if the user has provided billing information (e.g., credit card or PayPal).
        """
        return any([self.credit_card_number, self.paypal_email, self.mpesa_phone_number])

    # Backref relationships
    customers = db.relationship(
        'Customer', backref='user_customers', lazy=True)
    orders = db.relationship('Orders', backref='user', lazy=True)


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    storage_space_id = db.Column(db.Integer, db.ForeignKey(
        'storage_space.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'order_status.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)

    # Renamed for clarity
    booking_date = db.Column(db.DateTime, nullable=False)  # New field
    booking_status = db.Column(db.String, nullable=False)  # New field

    total_price = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String, nullable=False)

    # Rename for clarity
    pickup_date_scheduled = db.Column(
        db.DateTime, nullable=False)  # Scheduled pickup date
    pickup_date_actual = db.Column(
        db.DateTime, nullable=False)  # Actual pickup date

    # Added a field to reference the selected storage unit
    pickup_space_id = db.Column(db.Integer, db.ForeignKey(
        'storage_space.id'), nullable=True)  # Nullable

    # Create a relationship with pick-up services
    pickups = db.relationship(
        'PickupService', backref='pickup_orders', lazy=True)

    # Define the foreign key relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    # Define the relationship to Discounts
    discounts = db.relationship('Discount', back_populates='order')

    # Define relationships for related entities (transactions, files, etc.)
    transactions = db.relationship('Transactions', backref='order', lazy=True)
    files = db.relationship('Files', backref='order', lazy=True)
    receipts = db.relationship('Receipts', backref='order', lazy=True)
    to_be_received_items = db.relationship(
        'To_be_received', backref='order', lazy=True)
    to_be_picked_items = db.relationship(
        'To_be_picked', backref='order', lazy=True)
    reviews = db.relationship('Reviews', backref='order', lazy=True)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    user = db.relationship('User', backref='customer')
    orders = db.relationship('Orders', backref='customer')


class Storage_space(db.Model):
    __tablename__ = 'storage_space'
    id = db.Column(db.Integer, primary_key=True)
    storage_space_id = db.Column(db.Integer, unique=True, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'storage_location.id'), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    orders = db.relationship('Orders', backref='storage_space',
                             lazy=True, foreign_keys='Orders.storage_space_id')
    slots = db.relationship('StorageSlot', backref='storage_space', lazy=True)

    def is_booked(self):
        """
        Check if the storage unit is currently booked.
        """
        return any(order.is_active() for order in self.orders)

    def is_available(self):
        """
        Check if the storage unit is available for booking.
        """
        return not self.is_booked()

    def mark_as_available(self):
        """
        Mark the storage unit as available when a booking expires or is terminated.
        """
        self.availability = True
        db.session.commit()

    def mark_as_booked(self):
        """
        Mark the storage unit as booked when a customer makes a booking.
        """
        self.availability = False
        db.session.commit()

    def calculate_price(self):
        """
        Calculate the price for this storage unit based on its size.
        Additional pricing logic can be added here, such as pricing tiers.
        """
        # Example: Calculate price based on size (you can adjust this logic)
        prices = {'Small': 50.00, 'Medium': 100.00, 'Large': 150.00}
        # Handle unknown sizes with a default value
        return prices.get(self.size, 0.00)

    def update_price(self):
        """
        Update the price of the storage unit based on its size.
        """
        self.price = self.calculate_price()
        db.session.commit()


class Storage_location(db.Model):
    __tablename__ = 'storage_location'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    storage_spaces = db.relationship(
        'Storage_space', backref='location', lazy=True)


class Order_status(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    orders = db.relationship('Orders', backref='order_status', lazy=True)


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, unique=True, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class Receipts(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, unique=True, nullable=False)
    receipt_date = db.Column(db.DateTime, nullable=False)
    receipt_amount = db.Column(db.Float, nullable=False)
    receipt_number = db.Column(db.String, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class To_be_received(db.Model):
    __tablename__ = 'to_be_received'
    id = db.Column(db.Integer, primary_key=True)
    to_be_received_id = db.Column(db.Integer, unique=True, nullable=False)
    item_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class To_be_picked(db.Model):
    __tablename__ = 'to_be_picked'
    id = db.Column(db.Integer, primary_key=True)
    to_be_picked_id = db.Column(db.Integer, unique=True, nullable=False)
    item_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)


class Discount(db.Model):
    __tablename__ = 'discounts'
    id = db.Column(db.Integer, primary_key=True)
    discount_id = db.Column(db.Integer, unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    order = db.relationship('Orders', back_populates='discounts')


class PickupService(db.Model):
    __tablename__ = 'pickup_services'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    # Fields to store pick-up service information
    pickup_date = db.Column(db.DateTime, nullable=False)
    pickup_address = db.Column(db.String, nullable=False)

    # Define valid values for pickup_status using a set
    VALID_PICKUP_STATUSES = {'Scheduled',
                             'In Progress', 'Completed', 'Canceled'}

    pickup_status = db.Column(db.String, nullable=False)

    # Add a relationship to the Orders table
    order = db.relationship('Orders', backref='pickup_service', lazy=True)

    def __init__(self, order_id, pickup_date, pickup_address, pickup_status):
        if pickup_status not in self.VALID_PICKUP_STATUSES:
            raise ValueError(
                f"Invalid pickup_status: {pickup_status}. Must be one of {', '.join(self.VALID_PICKUP_STATUSES)}")

        self.order_id = order_id
        self.pickup_date = pickup_date
        self.pickup_address = pickup_address
        self.pickup_status = pickup_status


class Notifications(db.Model):
    """
    Model for user notifications.
    """
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    notification_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User', backref='notifications', lazy=True)


class Logs(db.Model):
    """
    Model for logging user actions.
    """
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    action = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    user = db.relationship('User', backref='logs', lazy=True)


class Closed_orders(db.Model):
    __tablename__ = 'closed_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    close_reason = db.Column(db.String, nullable=False)
    closure_date = db.Column(db.DateTime, nullable=False)
    order = db.relationship('Orders', backref='closed_order', lazy=True)


class StorageSlot(db.Model):
    __tablename__ = 'storage_slots'
    id = db.Column(db.Integer, primary_key=True)
    storage_space_id = db.Column(db.Integer, db.ForeignKey(
        'storage_space.id'), nullable=False)
    slot_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    availability = db.Column(db.Boolean, nullable=False, default=True)

    # Define a self-referential relationship for child slots
    parent_slot_id = db.Column(db.Integer, db.ForeignKey('storage_slots.id'))
    child_slots = db.relationship('StorageSlot', backref=db.backref(
        'parent_slot', remote_side=id), lazy='dynamic')
