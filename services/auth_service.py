from models.users import User
from config.db_init import db
from common.helper import userModel_to_user
from common.utils import createToken
from common.constants.app_constant import Role

def loginUser(request):
    userEmail = request.json.get("email",None)
    password = request.json.get("password",None)
    user = User.query.filter_by(email = userEmail).first()
    if user and user.password_hash == password:
        return {'token' : createToken(user)}
    
    
def signupUser(request):
    userEmail = request.json.get("email",None)
    password = request.json.get("password",None)
    userName = request.json.get("username",None)
    userRole = request.json.get("role",Role.CLIENT.value)
    newUser = User(email = userEmail,
                   password_hash = password,
                   username = userName,
                   role = userRole)
    db.session.add(newUser)
    db.session.commit()
    userInfo = userModel_to_user(newUser)
    return {'user' : userInfo , 'token' : createToken(newUser)}