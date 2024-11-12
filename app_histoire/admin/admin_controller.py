from app import app
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from dataclasses import dataclass
from .admin_service import get_user_data, set_user_data, delete_user_data
from common.validators.request_role_auth import role_required
from common.constants.app_constant import Role, MessageCode
from common.utils import is_value_bool_true


@dataclass
class GetUserRequest:
    """request structure for get request to get user data"""
    page_no: int
    page_size: int
    deleted: bool


@app.route('/getUsers', methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def get_users():
    """get users data"""
    try:
        page_number: int = request.args.get('pageNo', 1, type=int)
        page_size: int = request.args.get('pageSize', 10, type=int)
        delete: bool = request.args.get('deleted', default=False,
                                        type=is_value_bool_true)
        users_as_dicts = get_user_data(page_number, page_size, delete)
        if not users_as_dicts:
            response_data = {
                'message': 'Task Received!',
                'message_code': MessageCode.NO_DATA.value,
                'data': users_as_dicts
                }
        else:
            response_data = {
                'message': 'Task Received!',
                'message_code': MessageCode.SUCCESS.value,
                'data': users_as_dicts
                }
        response = make_response(response_data, 200)
    except Exception:
        response_data = {
            'message': 'Task could not be Retrived!',
            'message_code': MessageCode.NOT_FOUND.value,
            'data': ''
            }
        response = make_response(response_data, 400)
    return response


@app.route('/updateUsers', methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def set_users():
    """update and set data of users"""
    try:
        update_request = request.get_json()
        user_resp = set_user_data(
            update_request['userId'], update_request['role'],
            update_request['deleted'])
        response_data = {
            'message': 'Task Saved!',
            'message_code': MessageCode.ACCEPTED.value,
            'data': user_resp
            }
        response = make_response(response_data, 201)
    except Exception:
        response_data = {
            'message': 'Task Could not be saved!',
            'message_code': MessageCode.ERROR.value,
            'data': ''
            }
        response = make_response(response_data, 400)
    return response


@app.route('/deleteUsers/<int:user_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.ADMIN.value)
def delete_users(user_id):
    """delete users data on the basis of user identifier"""
    try:
        delete_user_data(user_id)
        response_data = {
            'message': 'User & Tasks Deleted!',
            'message_code': MessageCode.SUCCESS.value,
            'data': ''
            }
        response = make_response(response_data, 200)
    except Exception:
        response_data = {
            'message': 'User Could not be deleted!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response
