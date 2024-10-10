from flask_jwt_extended import JWTManager

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = 'todox'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    jwt = JWTManager(app)
    return jwt