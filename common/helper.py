def task_to_dict(task):
    return {
        'id': task.id,
        'userId': task.userId,
        'task': task.task,
        'status': task.status
    }