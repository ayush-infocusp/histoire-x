from flask_jwt_extended import create_access_token

def createToken(user):
    access_token = create_access_token(identity = user.id)
    return access_token