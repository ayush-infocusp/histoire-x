from flask_jwt_extended import create_access_token, get_jwt


def create_token(user):
    """create the token wrt the user details"""
    additional_claims = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
            }
    access_token = create_access_token(identity=str(user.id),
                                       additional_claims=additional_claims)
    return access_token


def is_value_bool_true(value):
    """check if the value is true"""
    return value.lower() == 'true'


def get_data_from_token(key):
    """get the user role if valid jwt"""
    jwt_data = get_jwt()
    user_role = jwt_data.get(key, "-")
    return user_role
