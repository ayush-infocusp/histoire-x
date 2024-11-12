import os
from flask import Flask, jsonify, make_response
from config.db_init import init_db
from config.jwt_init import init_jwt
from flask_cors import CORS
from common.common_exception import CommonAppException
import werkzeug


basedir = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = 'upload_data'


from speech_recog import *


app = Flask(__name__)
# setup the db config
db = init_db(app, basedir)

from controller.client_controller import *
from controller.auth_contoller import *
from controller.admin_controller import *
from common.interceptor import *


# setup the jwt
jwt = init_jwt(app)
CORS(app, support_credentials=True)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    """error response for all the unauthorised users"""
    return jsonify({
        'message_code': 'E20401',
        'message': 'Missing Authorization Header',
        'data': ''
    }), 401
    # raise CommonAppException("Missing Authorization Header 1", status_code=401) from Exception


@app.errorhandler(CommonAppException)
def handle_custom_exception(error):
    """handle the custom exception"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return make_response(response)


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return jsonify({
        'message_code': 'E20401',
        'message': 'Are you looking for something cooler!!??',
        'data': ''
    }), 403


if __name__ == '__main__':
    app.run(debug=True)
