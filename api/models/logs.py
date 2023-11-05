from datetime import datetime
from api.app import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='logs')

    def __init__(self, user_id, action, description=None):
        self.user_id = user_id
        self.action = action
        self.description = description

    def __str__(self):
        return f"User #{self.user_id} performed '{self.action}' at {self.timestamp}"
