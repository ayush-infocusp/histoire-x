import os
from flask import Flask, jsonify, make_response, send_from_directory
from config.db_init import init_db
from config.jwt_init import init_jwt
from flask_cors import CORS
from common.common_exception import CommonAppException
import werkzeug


basedir = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = 'upload_data'

# register speech recog model
from speech_recog import *


app = Flask(__name__, static_folder='./static/todo_app', static_url_path='/')
# setup the db config
db = init_db(app, basedir)


@app.route('/')
def index_html():
    return send_from_directory(app.static_folder, 'index.html')


#register bluerpints
from app_histoire.main import bp as main_bp
app.register_blueprint(main_bp)

from app_histoire.client import bp as client_bp
app.register_blueprint(client_bp, url_prefix='/app')

from app_histoire.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')


# register interceptor
from common.interceptor import *


# setup the jwt
jwt = init_jwt(app)
CORS(app, support_credentials=True)


@app.errorhandler(CommonAppException)
def handle_custom_exception(error):
    """handle the custom exception"""
    if isinstance(error, CommonAppException):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return make_response(response)
    else:
        return jsonify({
            'message_code': 'E20400',
            'message': 'Something Went Wrong!!??',
            'data': ''
        }), 400
# elif isinstance(error, RuntimeError)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    """error response for all the unauthorised users"""
    return jsonify({
        'message_code': 'E20401',
        'message': 'Missing Authorization Header',
        'data': ''
    }), 401
    # raise CommonAppException("Missing Authorization Header 1", status_code=401)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return jsonify({
        'message_code': 'E20401',
        'message': 'Are you looking for something cooler!!??',
        'data': ''
    }), 403


if __name__ == '__main__':
    app.run(debug=True)


# import logging
# logging.basicConfig()
# logging.info()
