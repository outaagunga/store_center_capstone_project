from models.database import db


class StorageSpace(db.Model):
    __tablename__ = 'storage_spaces'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    size = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_month = db.Column(db.Float(precision=2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float(precision=6), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)

    # Relationships
    # user = db.relationship('User', back_populates='storage_spaces')
    # bookings = db.relationship('Booking', back_populates='space')

    def __init__(self, user_id, name, size, capacity, price_per_month, address, latitude, longitude, description=None, available=True):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.size = size
        self.capacity = capacity
        self.price_per_month = price_per_month
        self.available = available
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.name} ({self.size}), {self.address}"
