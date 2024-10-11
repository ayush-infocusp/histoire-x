import os
from flask import Flask , jsonify
from config.db_init import init_db , init_models 
from config.jwt_init import init_jwt
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# setup the db config
db = init_db(app,basedir)

from controller.clientController import *
from controller.authContoller import *

#set model initialisation for not re-creating new models always
models_initialized = False
# setup the jwt
jwt = init_jwt(app)
CORS(app, support_credentials=True)

@app.before_request
def before_request():
    global models_initialized
    if not models_initialized:
        init_models(app,db)
        models_initialized = True
        
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'mc': '20401',
        'm': 'Missing Authorization Header',
        'dt' : ''
    }), 401

if __name__ == '__main__':
    app.run(debug=True)