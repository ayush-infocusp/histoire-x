from app import app
from services.auth_service import loginUser, signupUser
from flask import request, make_response
from flask_cors import cross_origin
from common.constants.app_constant import MessageCode


@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    try:
        taskResp = loginUser(request)
        responseData = {'m': 'User LoggedIn!',
                        'mc': MessageCode.CREATED.value,
                        'dt': taskResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'m': 'User cred not valid!',
                        'mc': MessageCode.ERROR.value,
                        'dt': taskResp}
        response = make_response(responseData, 400)
    return response


@app.route('/signup', methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    try:
        taskResp = signupUser(request)
        responseData = {'m': 'User onboarded!',
                        'mc': MessageCode.CREATED.value,
                        'dt': taskResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'m': 'User Could not be saved!',
                        'mc': MessageCode.ERROR.value,
                        'dt': ''}
        response = make_response(responseData, 400)
    return response
