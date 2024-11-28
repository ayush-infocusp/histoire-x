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


def delete_user_data(user_id: int):
    """delete user data on the basis of identifer"""
    user = User.get_user_by_id(user_id)
    if user:
        user.deleted = True
        tasks = db.session.query(Task).filter(Task.userId == user_id).all()
        for task in tasks:
            task.deleted = True
        db.session.commit()
