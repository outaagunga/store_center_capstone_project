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
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(300))
    address = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    orders = db.relationship('Order', backref='customer',
                             foreign_keys='Order.customer_id')

    customer = db.relationship(
        'Customer', back_populates='user', uselist=False)

    def __init__(self, full_name, username, email, phone_number, password, role, public_id=None,
                 profile_picture=None, address=None):
        self.public_id = public_id
        self.full_name = full_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role
        self.profile_picture = profile_picture
        self.address = address


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    storage_space_id = db.Column(db.Integer, db.ForeignKey(
        'storage_space.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'order_status.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    order_reference_code = db.Column(db.String(50), nullable=True)
    invoice = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    packed = db.Column(db.Boolean, nullable=True)
    shipped = db.Column(db.Boolean, nullable=True)
    number_of_items = db.Column(db.Integer, nullable=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    booking_status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    pickup_date_scheduled = db.Column(db.DateTime, nullable=False)
    pickup_date_actual = db.Column(db.DateTime, nullable=False)
    pickup_storage_space_id = db.Column(
        db.Integer, db.ForeignKey('storage_space.id'), nullable=True)

    # Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    user = db.relationship('User', back_populates='orders',
                           foreign_keys='Order.customer_id')

    storage_space = db.relationship(
        'StorageSpace', foreign_keys=[storage_space_id])

    order_status = db.relationship('OrderStatus', foreign_keys=[status_id])

    pickup_storage_space = db.relationship(
        'StorageSpace', foreign_keys='Order.pickup_storage_space_id')

    def __init__(self, order_id, customer_id, storage_space_id, status_id, order_date, delivery_date, total_price, booking_date, booking_status, payment_status, pickup_date_scheduled, pickup_date_actual):
        self.order_id = order_id
        self.customer_id = customer_id
        self.storage_space_id = storage_space_id
        self.status_id = status_id
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.total_price = total_price
        self.booking_date = booking_date
        self.booking_status = booking_status
        self.payment_status = payment_status
        self.pickup_date_scheduled = pickup_date_scheduled
        self.pickup_date_actual = pickup_date_actual


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    user = db.relationship('User', back_populates='customer')

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    def get_orders(self):
        """Returns a list of all orders for the customer."""
        # Assuming there is a one-to-many relationship between Customer and Order
        return self.orders

    def __init__(self, customer_id, user_id, first_name, last_name, date_of_birth=None, address=None, phone_number=None, email=None):
        self.customer_id = customer_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number
        self.email = email


# Storage_space

class StorageSpace(db.Model):
    __tablename__ = 'storage_space'
    id = db.Column(db.Integer, primary_key=True)
    storage_space_id = db.Column(db.Integer, unique=True, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'storage_location.id'), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)

    pickup_storage_space_id = db.Column(
        db.Integer, db.ForeignKey('storage_space.id'), nullable=True)
    pickup_storage_space = db.relationship('StorageSpace', remote_side=[
                                           id], primaryjoin="StorageSpace.pickup_storage_space_id == StorageSpace.id")

    def is_booked(self):
        """
        Check if the storage unit is currently booked.
        """
        # Implement your logic to check if it's booked (assuming you have the required relationships)

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

    def __init__(self, storage_space_id, size, price, location_id, availability=True):
        self.storage_space_id = storage_space_id
        self.size = size
        self.price = price
        self.location_id = location_id
        self.availability = availability


class StorageLocation(db.Model):
    __tablename__ = 'storage_location'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float(precision=6), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)
    # storage_spaces = db.relationship(
    #     'StorageSpace', backref='location', lazy=True)

    def __init__(self, location_id, name, address, latitude, longitude):
        self.location_id = location_id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    # orders = db.relationship('Order', backref='order_status')

    def __init__(self, status_id, name):
        self.status_id = status_id
        self.name = name


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, unique=True, nullable=False)
    transaction_code = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    def __init__(self, transaction_id, amount, transaction_date, order_id, transaction_code=None):
        self.transaction_id = transaction_id
        self.transaction_code = transaction_code
        self.amount = amount
        self.transaction_date = transaction_date
        self.order_id = order_id


class Receipts(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, unique=True, nullable=False)
    receipt_date = db.Column(db.DateTime, nullable=False)
    receipt_amount = db.Column(db.Float, nullable=False)
    receipt_number = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    def __init__(self, receipt_id, receipt_date, receipt_amount, receipt_number, order_id):
        self.receipt_id = receipt_id
        self.receipt_date = receipt_date
        self.receipt_amount = receipt_amount
        self.receipt_number = receipt_number
        self.order_id = order_id


class ToBeReceived(db.Model):
    __tablename__ = 'to_be_received'
    id = db.Column(db.Integer, primary_key=True)
    to_be_received_id = db.Column(db.Integer, unique=True, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    def __init__(self, to_be_received_id, item_name, quantity, order_id):
        self.to_be_received_id = to_be_received_id
        self.item_name = item_name
        self.quantity = quantity
        self.order_id = order_id


class ToBePicked(db.Model):
    __tablename__ = 'to_be_picked'
    id = db.Column(db.Integer, primary_key=True)
    to_be_picked_id = db.Column(db.Integer, unique=True, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    def __init__(self, to_be_picked_id, item_name, quantity, order_id):
        self.to_be_picked_id = to_be_picked_id
        self.item_name = item_name
        self.quantity = quantity
        self.order_id = order_id


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)

    def __init__(self, review_id, rating, comment, review_date, order_id):
        self.review_id = review_id
        self.rating = rating
        self.comment = comment
        self.review_date = review_date
        self.order_id = order_id


class Discount(db.Model):
    __tablename__ = 'discounts'
    id = db.Column(db.Integer, primary_key=True)
    discount_id = db.Column(db.Integer, unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    # order = db.relationship('Order', back_populates='discount')

    def __init__(self, discount_id, order_id, discount_amount, expiration_date):
        self.discount_id = discount_id
        self.order_id = order_id
        self.discount_amount = discount_amount
        self.expiration_date = expiration_date


# # PickupService

class PickupService(db.Model):
    __tablename__ = 'pickup_services'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    pickup_date = db.Column(db.DateTime, nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)

    pickup_status = db.Column(db.String(20), nullable=False)

    # Define valid values for pickup_status using a set
    VALID_PICKUP_STATUSES = {'Scheduled',
                             'In Progress', 'Completed', 'Canceled'}

    def __init__(self, order_id, pickup_date, pickup_address, pickup_status):
        if pickup_status not in self.VALID_PICKUP_STATUSES:
            raise ValueError(
                f"Invalid pickup_status: {pickup_status}. Must be one of {', '.join(self.VALID_PICKUP_STATUSES)}")

        self.order_id = order_id
        self.pickup_date = pickup_date
        self.pickup_address = pickup_address
        self.pickup_status = pickup_status

    def get_order(self):
        """Get the associated Order object."""
        # Retrieve the associated Order object using the order_id
        return Order.query.get(self.order_id)

    def set_order(self, order):
        """Set the associated Order object."""
        self.order_id = order.id
        db.session.commit()


class Notification(db.Model):
    """
    Model for user notifications.
    """
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    notification_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False, nullable=False)
    # user = db.relationship('User', backref='notifications', lazy=True)

    def __init__(self, notification_id, user_id, message):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message


class Log(db.Model):
    """
    Model for logging user actions.
    """
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=True)
    # user = db.relationship('User', backref='logs', lazy=True)

    def __init__(self, log_id, user_id, action):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action


class ClosedOrder(db.Model):
    __tablename__ = 'closed_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    close_reason = db.Column(db.String(255), nullable=False)
    closure_date = db.Column(db.DateTime, nullable=False)
    # order = db.relationship('Order', backref='closed_order', lazy=True)

    def __init__(self, order_id, close_reason, closure_date):
        self.order_id = order_id
        self.close_reason = close_reason
        self.closure_date = closure_date


class StorageSlot(db.Model):
    __tablename__ = 'storage_slots'
    id = db.Column(db.Integer, primary_key=True)
    storage_space_id = db.Column(db.Integer, db.ForeignKey(
        'storage_space.id'), nullable=False)
    slot_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))  # Specify data type and length
    availability = db.Column(db.Boolean, nullable=False, default=True)

    # Define a self-referential relationship for child slots
    parent_slot_id = db.Column(db.Integer, db.ForeignKey('storage_slots.id'))
    # child_slots = db.relationship('StorageSlot', backref=db.backref(
    #     'parent_slot', remote_side=id), lazy='dynamic')

    def __init__(self, storage_space_id, slot_number, description=None, availability=True):
        self.storage_space_id = storage_space_id
        self.slot_number = slot_number
        self.description = description
        self.availability = availability

