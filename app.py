import os
from flask import Flask, jsonify
from config.db_init import init_db
from config.jwt_init import init_jwt
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = 'upload_data'
app = Flask(__name__, static_folder=STATIC_FOLDER)
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
    return jsonify({
        'message_code': 'E20401',
        'message': 'Missing Authorization Header',
        'data': ''
    }), 401


if __name__ == '__main__':
    app.run(debug=True)
