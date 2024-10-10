from config.db_init import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))