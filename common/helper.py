def task_to_dict(task):
    return {
        'id': task.id,
        'userId': task.userId,
        'task': task.task,
        'status': task.status
    }
    
def userModel_to_user(user):
    return {
        'id' : user.id,
        'username' : user.username,
        'email' : user.email,
        'role' : user.role
    }