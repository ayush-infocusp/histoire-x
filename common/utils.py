from flask_jwt_extended import create_access_token, get_jwt

def createToken(user):
    additional_claims = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
            }
    access_token = create_access_token(identity=user.id,
                                       additional_claims=additional_claims)
    return access_token


def is_value_bool_true(value):
    return value.lower() == 'true'


def getDataFromToken(key):
    jwt_data = get_jwt()
    user_role = jwt_data.get(key, "-")
    return user_role
