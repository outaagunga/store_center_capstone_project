from datetime import datetime
from models.main import db


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    delivery_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    # Pending, Delivered, etc.
    delivery_status = db.Column(db.String(20), default='Pending')
    

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='delivery', lazy=True)
    


from datetime import datetime
from models.main import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
   

    # Define a one-to-many relationship with Stored Items
    stored_items = db.relationship('StoredItem', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    deliveries = db.relationship('Delivery', backref='user', lazy=True)
    pickups = db.relationship('Pickup', backref='user', lazy=True)
    shipping = db.relationship('Shipping', backref='user', lazy=True)

from datetime import datetime
from models.main import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'stored_items.item_id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # In or Out
    timestamp = db.Column(db.DateTime, nullable=False)
   

    delivery_id = db.Column(
        db.Integer, db.ForeignKey('deliveries.delivery_id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickups.pickup_id'))
    shipping_id = db.Column(db.Integer, db.ForeignKey('shippings.shipping_id'))

    stored_item = db.relationship(
        'StoredItem', back_populates='transactions', lazy=True)
    delivery = db.relationship(
        'Delivery', backref='transaction', uselist=False)
    pickup = db.relationship(
        'Pickup', backref='transaction', uselist=False)
    shipping = db.relationship(
        'Shipping', backref='transaction', uselist=False)
   

from datetime import datetime
from models.main import db


class StoredItem(db.Model):
    __tablename__ = 'stored_items'

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey(
        'warehouse_spaces.space_id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))  # Store the path to the image
    status = db.Column(db.String(20), default='In')  # In, Out, etc.
    

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='stored_item', lazy=True)

from datetime import datetime
from models.main import db


class Shipping(db.Model):
    __tablename__ = 'shippings'

    shipping_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    # Pending, Shipped, Delivered, etc.
    shipping_status = db.Column(db.String(20), default='Pending')
   

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='shipping', lazy=True)

from datetime import datetime
from models.main import db


class Receipt(db.Model):
    __tablename__ = 'receipts'

    receipt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.transaction_id'), nullable=False)
    # e.g., Storage, Delivery, Pickup
    receipt_type = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
   

    # Define a many-to-one relationship with User
    user = db.relationship('User', backref='receipts')

    # Define a many-to-one relationship with Transaction
    transaction = db.relationship('Transaction', backref='receipts')

from datetime import datetime
from models.main import db


class Pickup(db.Model):
    __tablename__ = 'pickups'

    pickup_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    # Pending, Completed, etc.
    pickup_status = db.Column(db.String(20), default='Pending')
   

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='pickup', lazy=True)

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import marshmallow
from flask_marshmallow import Marshmallow


app = Flask(__name__)


app.config['SECRET_KEY'] = 'opuyoapuga',
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:975129216@localhost/storecenter'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy()
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from datetime import datetime
from models.main import db


class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'stored_items.item_id'), nullable=False, unique=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    # Set default to current timestamp
    date_to_warehouse = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=True)
    description = db.Column(db.Text, nullable=True)

    stored_item = db.relationship(
        'StoredItem', backref='inventory', uselist=False)