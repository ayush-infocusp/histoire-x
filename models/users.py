from config.db_init import db
from datetime import datetime
from typing import List
from uuid import uuid4
from models.tasks import Task


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', cascade="all,delete", backref='User')
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_users_by_status(self, page_size: int, offset_value: int, delete: bool) -> List['User']:
        """get users on the basis of status"""
        stmt = db.select(User).filter_by(deleted=delete).limit(page_size).offset(offset_value)
        user_lists = db.session.execute(stmt).scalars().all()
        return user_lists

    def get_user_by_id(self, user_id: int) -> 'User':
        """get user data on the basis of identifer"""
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.execute(stmt).scalars().one()
        return user
