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
        responseData = {'message': 'User LoggedIn!',
                        'message_code': MessageCode.CREATED.value,
                        'data': taskResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'message': 'User cred not valid!',
                        'message_code': MessageCode.ERROR.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response


@app.route('/signup', methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    try:
        taskResp = signupUser(request)
        responseData = {'message': 'User onboarded!',
                        'message_code': MessageCode.CREATED.value,
                        'data': taskResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'message': 'User Could not be saved!',
                        'message_code': MessageCode.ERROR.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response
