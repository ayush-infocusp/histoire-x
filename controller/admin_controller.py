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
            responseData = {'m': 'Task Received!',
                            'mc': MessageCode.NO_DATA.value,
                            'dt': users_as_dicts}
        else:
            responseData = {'m': 'Task Received!',
                            'mc': MessageCode.SUCCESS.value,
                            'dt': users_as_dicts}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'m': 'Task could not be Retrived!',
                        'mc': MessageCode.NOT_FOUND.value,
                        'dt': ''}
        response = make_response(responseData, 400)
    return response


@app.route('/admin/updateUsers', methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def setUsers():
    # try:
        updateRequest = request.get_json()
        userResp = setUserData(updateRequest['userId'], updateRequest['role'], updateRequest['deleted'])
        responseData = {'m': 'Task Saved!',
                        'mc': MessageCode.ACCEPTED.value,
                        'dt': userResp}
        response = make_response(responseData, 201)
        return response
    # except Exception:
        # responseData = {'m': 'Task Could not be saved!',
                        # 'mc': MessageCode.ERROR.value,
                        # 'dt': ''}
        # response = make_response(responseData, 400)
    # return response


@app.route('/admin/deleteUsers/<int:user_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def deleteUsers(user_id):
    try:
        deleteUserData(user_id)
        responseData = {'m': 'User & Tasks Deleted!',
                        'mc': MessageCode.SUCCESS.value,
                        'dt': ''}
        response = make_response(responseData, 200)
    except Exception:
        responseData = {'m': 'User Could not be deleted!',
                        'mc': MessageCode.ERROR.value,
                        'dt': ''}
        response = make_response(responseData, 400)
    return response
