import os
from flask_sqlalchemy import SQLAlchemy


# global database obj
db = None


def init_db(app, basedir):
    """set up the database config"""
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'todox.db')
    db = SQLAlchemy(app)
    return db
