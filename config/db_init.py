import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = None

def init_db(app,basedir):
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'todox.db')
    db = SQLAlchemy(app)
    return db

def init_models(app,db):
    with app.app_context():
        db.create_all()