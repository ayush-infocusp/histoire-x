from app import app
from services.app_service import getUserData , setUserData , deleteUserData
from flask import request ,make_response 
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required
    
@app.route('/admin/getUsers',methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
def getUsers():
    try:
        users_as_dicts = getUserData(request)
        print(users_as_dicts)
        if not users_as_dicts:
            responseData = {'m': 'Task Received!','mc' :'S20004','dt' :users_as_dicts}
        else:
            responseData = {'m': 'Task Received!','mc' :'S20000','dt' :users_as_dicts}
        response = make_response(responseData, 200)
        # return response
    except Exception as e:
        responseData = {'m': 'Task could not be Retrived!','mc' :'S20404','dt' : ''}
        response = make_response(responseData, 400)
    return response

@app.route('/admin/setUsers',methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def setUsers():
    try:
        userResp = setUserData(request)
        responseData = {'m': 'Task Saved!','mc' :'S20001','dt' :userResp}
        response = make_response(responseData, 201)
    except Exception as e:
        responseData = {'m': 'Task Could not be saved!','mc' :'S20404','dt' :userResp}
        response = make_response(responseData, 400)
    return response

@app.route('/admin/deleteUsers/<int:user_id>',methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
def deleteUsers(user_id):
    try:
        userResp = deleteUserData(user_id)
        responseData = {'m': 'Task Deleted!','mc' :'S20000','dt' : ''}
        response = make_response(responseData, 200)
    except Exception as e:
        responseData = {'m': 'Task Could not be deleted!','mc' :'S20404','dt' :userResp}
        response = make_response(responseData, 400)
    return response
