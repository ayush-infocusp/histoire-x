import os
from config.db_init import db
from models.tasks import Task
from models.users import User
from speech_recog import get_speech_details
from common.audio_helper import convert_audio_puarray
from common.helper import task_to_dict, userModel_to_user
from common.utils import get_data_from_token
from common.constants.app_constant import Role, Status, tasksType
from common.models.request_model import GetTodosRequest, SetTodosRequest


UPLOAD_DIR = "upload_data"
# Directory to store temporary files

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


# get the todos on the basis of the user
def get_todos(request: GetTodosRequest):
    """get the todos data on per user basis"""
    page_number = request.pageNo
    page_size = request.pageSize
    user_code = str(get_data_from_token('id'))
    status = request.status
    if status and status not in [s.value for s in Status]:
        return Exception("status not acceptable")
    offset_value = (page_number - 1) * page_size
    if status:
        stmt = db.select(Task).filter_by(userId=user_code,
                                         status=status,
                                         deleted=False).limit(page_size).offset(offset_value)
    else:
        stmt = db.select(Task).filter_by(userId=user_code, deleted=False).limit(page_size).offset(offset_value)
    task_lists = db.session.execute(stmt).scalars().all()
    tasks_as_dicts = [task_to_dict(task) for task in task_lists]
    return tasks_as_dicts


# set the todo item wrt the user identifer
def set_todos(request: SetTodosRequest):
    """set the todos for the user"""
    try:
        user_code = str(get_data_from_token('id'))
        task = Task(userId=user_code,
                    task=request.task,
                    status=request.status)
        db.session.add(task)
        db.session.commit()
        task_response = task_to_dict(task)
        # text = get_speech_details()
    except Exception:
        print("exception")
    return {"task_response": task_response, "text": request.task}


# update specific todo item on the basis of task identifier
def update_todos(request):
    """update specific todo item on the basis of task identifier"""
    task_request = request.get_json()
    user_code = str(get_data_from_token('id'))
    task = db.session.query(Task).filter(
        Task.id == task_request['id'],
        Task.userId == user_code).one_or_none()
    if not task:
        return Exception("selected data is invalid")
    task.status = task_request['status']
    db.session.commit()
    task_response = task_to_dict(task)
    return task_response


# soft delete specific todo item on the basis of task identifier
def delete_todos(task_id):
    """delete todos with soft delete on the basis of task id"""
    task = db.session.query(Task).filter(Task.id == task_id).one()
    task.deleted = True
    db.session.commit()


# get the users on the basis of the roles and deleted
def get_user_data(page_number: int, page_size: int, delete: bool):
    """get user data on the basis of delted filter"""
    offset_value = (page_number - 1) * page_size
    user_lists = User.get_users_by_status(page_size, offset_value, delete)
    user_dicts = [userModel_to_user(user) for user in user_lists]
    return user_dicts


def set_user_data(user_id: int, role: Role, deleted: bool):
    """set user data"""
    user = User.get_user_by_id(user_id)
    if user:
        user.role = role
        user.deleted = deleted
        db.session.commit()
        return userModel_to_user(user)
    else:
        return None


def delete_user_data(user_id):
    """delete user data on the basis of identifer"""
    user = User.get_user_by_id(user_id)
    if user:
        user.deleted = True
        tasks = db.session.query(Task).filter(Task.userId == user_id).all()
        for task in tasks:
            task.deleted = True
        db.session.commit()


def upload_file(request):
    """upload file and save in local"""
    is_multipart = request.form.get('is_multipart') == 'true'
    file_type = request.form.get('file_type')
    if "file_chunk" not in request.files:
        return 'No file part!'
    file = request.files['file_chunk']
    text = None
    if file.filename == '':
        return 'No selected file'
    # to save file with specific name
    to_save_filename = file.filename + " | TEXT :- "
    if not is_multipart:
        text = text_to_speech_single_part(file, file_type, to_save_filename)
    else:
        text = file_upload_not_multipart(file, request, file_type, to_save_filename)
    return {
        "message": 'File uploaded successfully!',
        "text": text
        }


def text_to_speech_single_part(file, file_type, to_save_filename):
    """text to speech processor for speech of single part file"""
    final_filepath = file_upload_not_multipart(
            file, file.filename)
    # get speech to text
    if file_type == tasksType.AUDIO.value:
        file_data = convert_audio_puarray(final_filepath['final_filepath'])
        text = get_speech_details(file_data['audio_data'])
        to_save_filename = to_save_filename + text['prediction']
    set_todos_for_file(to_save_filename, file_type)
    return text


def text_to_speech_multipart(file, request, file_type, to_save_filename):
    """text to speech processor for speech of multi part file"""
    multipart_upload_data = file_upload_multipart(
        file, file.filename, request)
    is_last_chunk = request.form.get(
        'is_last_chunk', 'false').lower() == 'true'
    # if multipart upload and is last chunk and save as final part data
    if multipart_upload_data and is_last_chunk:
        # get speech to text if file type is audio
        if file_type == tasksType.AUDIO.value:
            final_filepath = multipart_upload_data['final_filepath']
            file_data = convert_audio_puarray(final_filepath)
            text = get_speech_details(file_data['audio_data'])
            to_save_filename = to_save_filename + text['prediction']
        get_user_file_valid(to_save_filename, file_type)
    return text


def file_upload_not_multipart(file, file_name):
    """file upload as single part data"""
    filepath = os.path.join(UPLOAD_DIR, f'{file_name}')
    file.save(filepath)
    return {
        "message": "File received successfully",
        "final_filepath": filepath
        }


def file_upload_multipart(file, original_filename, request):
    """file upload as multi part data """
    file_id = request.form.get('file_id')
    is_last_chunk = request.form.get(
        'is_last_chunk', 'false').lower() == 'true'
    # file_type = request.form.get('file_type')
    temp_filepath = os.path.join(
        UPLOAD_DIR, f"{file_id}_{original_filename}.part")
    with open(temp_filepath, 'ab') as f:
        f.write(file.read())

    final_filepath = None
    if is_last_chunk:
        final_filepath = os.path.join(UPLOAD_DIR, original_filename)
        os.rename(temp_filepath, final_filepath)
        print(f"File {original_filename} uploaded successfully!")
    return {
        "message": "Chunk received successfully",
        "final_filepath": final_filepath
        }


def set_todos_for_file(original_filename, file_type):
    """set the todos for the file"""
    user_code = str(get_data_from_token('id'))
    task = Task(userId=user_code,
                task=original_filename,
                status=Status.PENDING.value,
                type=file_type)
    db.session.add(task)
    db.session.commit()


def get_user_file_valid(user_code: str, path: str):
    """get if the file requested by the user is valid"""
    if user_code and path:
        tasks = db.session.query(Task).filter(
            Task.userId == user_code, Task.task == path).all()
        if tasks:
            return True
    return False
