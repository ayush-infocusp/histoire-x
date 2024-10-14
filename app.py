import os
from flask import Flask , jsonify
from config.db_init import init_db , init_models 
from config.jwt_init import init_jwt
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# setup the db config
db = init_db(app,basedir)
init_models(app,db)

from controller.client_controller import *
from controller.auth_contoller import *
from controller.admin_controller import *

# setup the jwt
jwt = init_jwt(app)
CORS(app, support_credentials=True)
        
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'mc': 'E20401',
        'm': 'Missing Authorization Header',
        'dt' : ''
    }), 401

if __name__ == '__main__':
    app.run(debug=True)