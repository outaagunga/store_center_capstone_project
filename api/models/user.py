from datetime import datetime
from models.database import db
from models.storagespace import StorageSpace
from models.review import Review
from models.notifications import Notification
from models.logs import Log


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(300))
    address = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    bio = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', back_populates='user', lazy=True)
    storage_spaces = db.relationship('StorageSpace', backref='user', lazy=True)
    # storage_locations = db.relationship(
    #     'StorageLocation', backref='user', lazy=True)
    # transactions = db.relationship('Transaction', backref='user', lazy=True)
    # receipts = db.relationship('Receipt', backref='user', lazy=True)
    # items_to_be_received = db.relationship(
    #     'ToBeReceived', backref='user', lazy=True)
    # items_to_be_picked = db.relationship(
    #     'ToBePicked', backref='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    # reviews = db.relationship('Review', backref='user', lazy=True)
    # discounts = db.relationship('Discount', backref='user', lazy=True)
    # pickup_services = db.relationship(
    #     'PickupService', backref='user', lazy=True)
    notifications = db.relationship(
        'Notification', back_populates='user', lazy=True)
    logs = db.relationship('Log', back_populates='user', lazy=True)
    # closed_orders = db.relationship('ClosedOrder', backref='user', lazy=True)
    # storage_slots = db.relationship('StorageSlot', backref='user', lazy=True)

    def __init__(self, public_id, full_name, username, email, phone_number, password, role, profile_picture=None, address=None, date_of_birth=None, gender=None, bio=None):
        self.public_id = public_id
        self.full_name = full_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.profile_picture = profile_picture
        self.address = address
        self.role = role
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.bio = bio

    def __str__(self):
        return f"User {self.username} ({self.email})"
