from config.db_init import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    
    def getUsersByStatus(pageSize,offset_value,delete):
        stmt = db.select(User).filter_by(deleted = delete).limit(pageSize).offset(offset_value)
        user_lists =  db.session.execute(stmt).scalars().all()
        return user_lists