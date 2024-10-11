from app import app
from services.authService import loginUser , signupUser
from flask import request ,make_response 
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin


@app.route('/login',methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    try:
        taskResp = loginUser(request)
        responseData = {'m': 'User LoggedIn!','mc' :'S20001','dt' :taskResp}
        response = make_response(responseData, 201)
    except Exception as e:
        responseData = {'m': 'User cred not valid!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

@app.route('/signup',methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    try:
        taskResp = signupUser(request)
        responseData = {'m': 'User onboarded!','mc' :'S20001','dt' :taskResp}
        response = make_response(responseData, 201)
    except Exception as e:
        responseData = {'m': 'User Could not be saved!','mc' :'S20404','dt' : ''}
        response = make_response(responseData, 400)
    return response