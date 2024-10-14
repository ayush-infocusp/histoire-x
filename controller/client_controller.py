from app import app
from services.app_service import getTodos , setTodos , updateTodos , deleteTodos
from flask import request ,make_response 
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required
from common.validators.request_role_auth import role_required
from common.constants.app_constant import Role
    
@app.route('/app/getTodos',methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def getUserTodos():
    try:
        tasks_as_dicts = getTodos(request)
        if not tasks_as_dicts:
            responseData = {'m': 'Task Received!','mc' :'S20004','dt' :tasks_as_dicts}
        else:
            responseData = {'m': 'Task Received!','mc' :'S20000','dt' :tasks_as_dicts}
        response = make_response(responseData, 200)
    except Exception as e:
        responseData = {'m': 'Task could not be Retrived!','mc' :'S20404','dt' : ''}
        response = make_response(responseData, 400)
    return response

@app.route('/app/setTodos',methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def setUserTodos():
    try:
        taskResp = setTodos(request)
        responseData = {'m': 'Task Saved!','mc' :'S20001','dt' :taskResp}
        response = make_response(responseData, 201)
    except Exception as e:
        responseData = {'m': 'Task Could not be saved!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

@app.route('/app/updateTodos',methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def updateUserTodos():
    try:
        taskResp = updateTodos(request)
        responseData = {'m': 'Task Saved!','mc' :'S20002','dt' : taskResp}
        response = make_response(responseData, 202)
    except Exception as e:
        responseData = {'m': 'Task Could not be updated!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

@app.route('/app/deleteTodos/<int:task_id>',methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def deleteUserTodos(task_id):
    try:
        taskResp = deleteTodos(task_id)
        responseData = {'m': 'Task Deleted!','mc' :'S20000','dt' : ''}
        response = make_response(responseData, 200)
    except Exception as e:
        responseData = {'m': 'Task Could not be deleted!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response
