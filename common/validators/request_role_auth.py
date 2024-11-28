from flask import make_response
from functools import wraps
from common.constants.app_constant import Role, MessageCode
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from common.common_exception import CommonAppException

allowed_roles = [Role.ADMIN.value, Role.CLIENT.value]


def role_required(restricted_role):
    """role is rquired and jwt is req"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # try:
                verify_jwt_in_request()
                jwt_data = get_jwt()
                user_role = jwt_data.get("role", "guest")
                print(user_role)
                if user_role not in allowed_roles or user_role != restricted_role :
                    raise CommonAppException('Access Denied: Insufficient Permissions!', status_code=401)
                return fn(*args, **kwargs)

            # except Exception as e:
            #     raise CommonAppException('Invalid Request', status_code=401) from e
        return wrapper
    return decorator
