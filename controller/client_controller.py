from app import app  # pylint: disable=import-error
from flask import request, make_response, send_from_directory
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_pydantic import validate

from services.app_service import get_todos, set_todos, update_todos, delete_todos, upload_file, get_user_file_valid

from common.utils import get_data_from_token
from common.validators.request_role_auth import role_required
from common.constants.app_constant import Role, MessageCode
from common.models.request_model import GetTodosRequest, SetTodosRequest


STATIC_FOLDER = 'upload_data'


@app.route('/app/todos', methods=["GET"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
@validate()
def get_user_todos(query: GetTodosRequest):
    """get the todos of users"""
    try:
        tasks_as_dicts = get_todos(query)
        if not tasks_as_dicts:
            response_data = {
                'message': 'Task Received!',
                'message_code': MessageCode.NO_DATA.value,
                'data': tasks_as_dicts}
        else:
            response_data = {
                'message': 'Task Received!',
                'message_code': MessageCode.SUCCESS.value,
                'data': tasks_as_dicts}
        response = make_response(response_data, 200)
    except Exception:
        response_data = {
            'message': 'Task could not be Retrived!',
            'message_code': MessageCode.ERROR.value,
            'data': str(tasks_as_dicts)}
        response = make_response(response_data, 400)
    return response


@app.route('/app/todos', methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
@validate()
def set_user_todos(body: SetTodosRequest):
    """set user todo data"""
    try:
        task_response = set_todos(body)
        response_data = {
            'message': 'Task Saved!',
            'message_code': MessageCode.CREATED.value,
            'data': task_response}
        response = make_response(response_data, 201)
    except Exception:
        response_data = {
            'message': 'Task Could not be saved!',
            'message_code': MessageCode.ERROR.value,
            'data': task_response}
        response = make_response(response_data, 400)
    return response


@app.route('/app/todos', methods=["PATCH"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def update_user_todos():
    """update the todos of the user"""
    try:
        task_response = update_todos(request)
        response_data = {
            'message': 'Task Updated!',
            'message_code': MessageCode.ACCEPTED.value,
            'data': task_response}
        response = make_response(response_data, 202)
    except Exception:
        response_data = {
            'message': 'Task Could not be updated!',
            'message_code': MessageCode.ERROR.value,
            'data': str(task_response)}
        response = make_response(response_data, 400)
    return response


@app.route('/app/todos/<int:task_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def delete_user_todos(task_id):
    """delete the todo of the user"""
    try:
        task_response = delete_todos(task_id)
        response_data = {
            'message': 'Task Deleted!',
            'message_code': MessageCode.SUCCESS.value,
            'data': task_response}
        response = make_response(response_data, 200)
    except Exception:
        response_data = {
            'message': 'Task Could not be deleted!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response


@app.route('/app/fileUpload', methods=["PUT"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def file_upload_todos():
    """upload file into the todos"""
    try:
        task_response = upload_file(request)
        response_data = {
            'message': 'File saved!',
            'message_code': MessageCode.SUCCESS.value,
            'data': task_response}
        response = make_response(response_data, 200)
        return response
    except Exception:
        response_data = {
            'message': 'File Could not be Saved!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response


@app.route('/send_file', methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
@role_required(Role.CLIENT.value)
def static_file():
    """get the static file data"""
    try:
        task_request = request.get_json()
        file_name = task_request['data']
        user_code = str(get_data_from_token('id'))
        is_valid = get_user_file_valid(user_code, file_name)
        if is_valid:
            return send_from_directory(STATIC_FOLDER,
                                       file_name.split(' | ')[0])
        else:
            response_data = {
                'message': 'File Could not be Retrived!',
                'message_code': MessageCode.NOT_FOUND.value,
                'data': ''}
            response = make_response(response_data, 404)
    except Exception:
        response_data = {
            'message': 'File Could not be Saved!',
            'message_code': MessageCode.ERROR.value,
            'data': ''}
        response = make_response(response_data, 400)
    return response
