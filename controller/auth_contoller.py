from app import app  # pylint: disable=import-error
from services.auth_service import login_user, signup_user  # pylint: disable=import-error
from flask import request, make_response  # pylint: disable=import-error
from flask_cors import cross_origin  # pylint: disable=import-error
from common.constants.app_constant import MessageCode  # pylint: disable=import-error


@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    """login the user"""
    try:
        task_response = login_user(request)
        response_data = {
            'message': 'User LoggedIn!',
            'message_code': MessageCode.CREATED.value,
            'data': task_response}
        response = make_response(response_data, 201)
    except Exception:
        response_data = {
            'message': 'User cred not valid!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response


@app.route('/signup', methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    """signup user"""
    try:
        task_response = signup_user(request)
        response_data = {
            'message': 'User onboarded!',
            'message_code': MessageCode.CREATED.value,
            'data': task_response}
        response = make_response(response_data, 201)
    except Exception:
        response_data = {
            'message': 'User Could not be saved!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response
