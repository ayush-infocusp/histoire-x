from models.users import User
from config.db_init import db
from common.helper import userModel_to_user
from common.utils import create_token
from common.constants.app_constant import Role


def login_user(request):
    """login user with creds"""
    userEmail = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=userEmail, deleted=False).first()
    if user and user.password_hash == password:
        return {'token': create_token(user)}


def signup_user(request):
    """signup user with creds"""
    user_email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_name = request.json.get("username", None)
    new_user = User(
        email=user_email,
        password_hash=password,
        username=user_name,
        role=Role.CLIENT.value)
    db.session.add(new_user)
    db.session.commit()
    user_info = userModel_to_user(new_user)
    return {'user': user_info, 'token': create_token(new_user)}
