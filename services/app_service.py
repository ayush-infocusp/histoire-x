from common.helper import task_to_dict, userModel_to_user
from config.db_init import db
from models.tasks import Task
from models.users import User
from common.constants.app_constant import Role, Status
from common.utils import getDataFromToken


# get the todos on the basis of the user
def getTodos(request):
    pageNumber = int(request.args.get('pageNo', 1))
    pageSize = int(request.args.get('pageSize', 10))
    userCode = str(getDataFromToken('id'))
    status = request.args.get('status')
    if status and status not in [s.value for s in Status]:
        return Exception("status not acceptable")
    offset_value = (pageNumber - 1) * pageSize
    if status:
        stmt = db.select(Task).filter_by(userId=userCode,
                                         status=status,
                                         deleted=False).limit(pageSize).offset(offset_value)
    else:
        stmt = db.select(Task).filter_by(userId=userCode, deleted=False).limit(pageSize).offset(offset_value)
    taskLists = db.session.execute(stmt).scalars().all()
    tasks_as_dicts = [task_to_dict(task) for task in taskLists]
    return tasks_as_dicts


# set the todo item wrt the user identifer
def setTodos(request):
    userCode = str(getDataFromToken('id'))
    taskRequest = request.get_json()
    task = Task(userId=userCode,
                task=taskRequest['task'],
                status=taskRequest['status'])
    db.session.add(task)
    db.session.commit()
    taskResp = task_to_dict(task)
    return taskResp


# update specific todo item on the basis of task identifier
def updateTodos(request):
    taskRequest = request.get_json()
    userCode = str(getDataFromToken('id'))
    task = db.session.query(Task).filter(Task.id == taskRequest['id'], Task.userId == userCode).one_or_none()
    if not task:
        return Exception("selected data is invalid")
    task.status = taskRequest['status']
    db.session.commit()
    taskResp = task_to_dict(task)
    return taskResp


# soft delete specific todo item on the basis of task identifier
def deleteTodos(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).one()
    task.deleted = True
    db.session.commit()


# get the users on the basis of the roles and deleted
def getUserData(pageNumber: int, pageSize: int, delete: bool):
    offset_value = (pageNumber - 1) * pageSize
    user_lists = User.getUsersByStatus(pageSize, offset_value, delete)
    user_dicts = [userModel_to_user(user) for user in user_lists]
    return user_dicts


def setUserData(user_id: int, role: Role, deleted: bool):
    user = User.getUserById(user_id)
    if user:
        user.role = role
        user.deleted = deleted
        db.session.commit()
        return userModel_to_user(user)
    else:
        return None


def deleteUserData(user_id):
    user = User.getUserById(user_id)
    if user:
        user.deleted = True
        tasks = db.session.query(Task).filter(Task.userId == user_id).all()
        for task in tasks:
            task.deleted = True
        db.session.commit()
