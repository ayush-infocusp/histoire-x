from app import app
from services.app_service import getUserData, setUserData, deleteUserData
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from common.validators.request_role_auth import role_required
from common.constants.app_constant import Role, MessageCode
from dataclasses import dataclass
from common.utils import is_value_bool_true


@dataclass
class GetUserRequest:
    page_no: int
    page_size: int
    deleted: bool


@app.route('/admin/getUsers', methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def getUsers():
    try:
        pageNumber: int = request.args.get('pageNo', 1, type=int)
        pageSize: int = request.args.get('pageSize', 10, type=int)
        delete: bool = request.args.get('deleted', default=False,
                                        type=is_value_bool_true)
        users_as_dicts = getUserData(pageNumber, pageSize, delete)
        if not users_as_dicts:
            responseData = {'message': 'Task Received!',
                            'message_code': MessageCode.NO_DATA.value,
                            'data': users_as_dicts}
        else:
            responseData = {'message': 'Task Received!',
                            'message_code': MessageCode.SUCCESS.value,
                            'data': users_as_dicts}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'message': 'Task could not be Retrived!',
                        'message_code': MessageCode.NOT_FOUND.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response


@app.route('/admin/updateUsers', methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def setUsers():
    try:
        updateRequest = request.get_json()
        userResp = setUserData(updateRequest['userId'], updateRequest['role'], updateRequest['deleted'])
        responseData = {'message': 'Task Saved!',
                        'message_code': MessageCode.ACCEPTED.value,
                        'data': userResp}
        response = make_response(responseData, 201)
    except Exception:
        responseData = {'message': 'Task Could not be saved!',
                        'message_code': MessageCode.ERROR.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response


@app.route('/admin/deleteUsers/<int:user_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def deleteUsers(user_id):
    try:
        deleteUserData(user_id)
        responseData = {'message': 'User & Tasks Deleted!',
                        'message_code': MessageCode.SUCCESS.value,
                        'data': ''}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'message': 'User Could not be deleted!',
                        'message_code': MessageCode.ERROR.value,
                        'data': ''}
        response = make_response(responseData, 400)
    return response
