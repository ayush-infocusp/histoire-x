from common.helper import task_to_dict
from config.db_init import db
from models.tasks import Task

# get the todos on the basis of the user
def getTodos(request):
    pageNumber = int(request.args.get('pageNo',1))
    pageSize = int(request.args.get('pageSize',10))
    userCode = str(request.headers.get('userCode'))
    status = request.args.get('status')
    offset_value = (pageNumber - 1) * pageSize
    if status:
        stmt = db.select(Task).filter_by(userId = userCode,status = status,deleted = False).limit(pageSize).offset(offset_value)
    else:
        stmt = db.select(Task).filter_by(userId = userCode,deleted = False).limit(pageSize).offset(offset_value)
    taskLists =  db.session.execute(stmt).scalars().all()
    tasks_as_dicts = [task_to_dict(task) for task in taskLists]
    return tasks_as_dicts

# set the todo item wrt the user identifer
def setTodos(request):
    userCode = request.headers.get('userCode') 
    taskRequest = request.get_json()
    task = Task(userId = userCode,
                task = taskRequest['data'],
                status = taskRequest['status'])
    db.session.add(task)
    db.session.commit()
    taskResp = task_to_dict(task)
    return taskResp

# update specific todo item on the basis of task identifier
def updateTodos(request):
    taskRequest = request.get_json()
    task = db.session.query(Task).filter(Task.id == taskRequest['id']).one()
    task.status = taskRequest['status']
    db.session.commit()
    taskResp = task_to_dict(task)
    return taskResp

# soft delete specific todo item on the basis of task identifier
def deleteTodos(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).one() 
    task.deleted = True
    db.session.commit()
        