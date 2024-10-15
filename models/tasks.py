from datetime import datetime
from config.db_init import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    task = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
