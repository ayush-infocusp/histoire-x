from app import app
from services.app_service import getTodos, setTodos, updateTodos, deleteTodos, uploadFile, getUserFileValid
from flask import request, make_response, send_from_directory
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from common.validators.request_role_auth import role_required
from common.constants.app_constant import Role, MessageCode
from common.utils import getDataFromToken

STATIC_FOLDER = 'upload_data'


@app.route('/app/todos', methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def getUserTodos():
    try:
        tasks_as_dicts = getTodos(request)
        if not tasks_as_dicts:
            responseData = {'message': 'Task Received!',
                            'message_code': MessageCode.NO_DATA.value,
                            'data': tasks_as_dicts}
        else:
            responseData = {'message': 'Task Received!',
                            'message_code': MessageCode.SUCCESS.value,
                            'data': tasks_as_dicts}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'message': 'Task could not be Retrived!',
                        'message_code': MessageCode.ERROR.value,
                        'data': str(tasks_as_dicts)}
        response = make_response(responseData, 400)
    return response


@app.route('/app/todos', methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def setUserTodos():
    try:
        taskResp = setTodos(request)
        responseData = {'message': 'Task Saved!',
                        'message_code': MessageCode.CREATED.value,
                        'data': taskResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'message': 'Task Could not be saved!',
                        'message_code': MessageCode.ERROR.value,
                        'data': taskResp}
        response = make_response(responseData, 400)
    return response


@app.route('/app/todos', methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def updateUserTodos():
    try:
        taskResp = updateTodos(request)
        print(taskResp)
        responseData = {'message': 'Task Updated!',
                        'message_code': MessageCode.ACCEPTED.value,
                        'data': taskResp}
        response = make_response(responseData, 202)
    except Exception:
        responseData = {'message': 'Task Could not be updated!',
                        'message_code': MessageCode.ERROR.value,
                        'data': str(taskResp)}
        response = make_response(responseData, 400)
    return response


@app.route('/app/todos/<int:task_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def deleteUserTodos(task_id):
    try:
        taskResp = deleteTodos(task_id)
        responseData = {'message': 'Task Deleted!',
                        'message_code': MessageCode.SUCCESS.value,
                        'data': ''}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'message': 'Task Could not be deleted!',
                        'message_code': MessageCode.ERROR.value,
                        'data': taskResp}
        response = make_response(responseData, 400)
    return response


@app.route('/app/fileUpload', methods=["PUT"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def fileUploadTodos():
    try:
        taskResp = uploadFile(request)
        responseData = {'message': 'File saved!',
                        'message_code': MessageCode.SUCCESS.value,
                        'data': taskResp}
        response = make_response(responseData, 200)
        return response
    except Exception:
        responseData = {'message': 'File Could not be Saved!',
                        'message_code': MessageCode.ERROR.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response


@app.route('/send_file', methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def static_file():
    # try:
        taskRequest = request.get_json()
        file_name = taskRequest['data']
        print(file_name , "hello")
        userCode = str(getDataFromToken('id'))
        is_valid = getUserFileValid(userCode, file_name)
        if is_valid:
            return send_from_directory(STATIC_FOLDER, file_name.split(' | ')[0])
        else:
            responseData = {'message': 'File Could not be Retrived!',
                            'message_code': MessageCode.NOT_FOUND.value,
                            'data': ''}
            response = make_response(responseData, 404)
            return response
    # except Exception:
    #     responseData = {'message': 'File Could not be Saved!',
    #                     'message_code': MessageCode.ERROR.value,
    #                     'data': ''}
    #     response = make_response(responseData, 400)
    #     return response
