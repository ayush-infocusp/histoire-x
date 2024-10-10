from flask import Flask , request ,make_response 
from config.db_init import init_db , init_models 
from config.jwt_init import init_jwt
from flask_jwt_extended import jwt_required

app = Flask(__name__)\
# setup the db config
db = init_db(app)

from services.appService import getTodos , setTodos , updateTodos , deleteTodos

#set model initialisation for not re-creating new models always
models_initialized = False
# setup the jwt
jwt = init_jwt(app)

@app.before_request
def before_request():
    global models_initialized
    if not models_initialized:
        init_models(app,db)
        models_initialized = True

@app.route('/app/getTodos',methods=["GET"])
@jwt_required()
def getUserTodos():
    try:
        tasks_as_dicts = getTodos(request)
        if tasks_as_dicts.size == 0:
            responseData = {'m': 'Task Received!','mc' :'S20004','dt' :tasks_as_dicts}
        else:
            responseData = {'m': 'Task Received!','mc' :'S20000','dt' :tasks_as_dicts}
        response = make_response(responseData, 200)
    except Exception as e:
        responseData = {'m': 'Task could not be Retrived!','mc' :'S20404','dt' : ''}
        response = make_response(responseData, 400)
    return response

@app.route('/app/setTodos',methods=["POST"])
def setUserTodos():
    try:
        taskResp = setTodos(request)
        responseData = {'m': 'Task Saved!','mc' :'S20001','dt' :taskResp}
        response = make_response(responseData, 201)
    except Exception as e:
        responseData = {'m': 'Task Could not be saved!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

@app.route('/app/updateTodos',methods=["PATCH"])
def updateUserTodos():
    try:
        taskResp = updateTodos(request)
        responseData = {'m': 'Task Saved!','mc' :'S20002','dt' : taskResp}
        response = make_response(responseData, 202)
    except Exception as e:
        responseData = {'m': 'Task Could not be updated!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

@app.route('/app/deleteTodos/<int:task_id>',methods=["DELETE"])
def deleteUserTodos(task_id):
    try:
        taskResp = deleteTodos(task_id)
        responseData = {'m': 'Task Deleted!','mc' :'S20000','dt' : ''}
        response = make_response(responseData, 200)
    except Exception as e:
        responseData = {'m': 'Task Could not be deleted!','mc' :'S20404','dt' :taskResp}
        response = make_response(responseData, 400)
    return response

if __name__ == '__main__':
    app.run(debug=True)