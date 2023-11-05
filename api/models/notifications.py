

from datetime import datetime
from api.app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    notification_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    user = db.relationship('User', back_populates='notifications')

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def mark_as_read(self):
        self.is_read = True

    def mark_as_unread(self):
        self.is_read = False

    def __str__(self):
        return f"Notification for User #{self.user_id}: {self.message}"
