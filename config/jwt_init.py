from flask_jwt_extended import JWTManager
import datetime


def init_jwt(app):
    """setup jwt configuration"""
    app.config["JWT_SECRET_KEY"] = 'todox'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    jwt = JWTManager(app)
    return jwt
