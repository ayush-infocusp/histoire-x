from flask import Blueprint

bp = Blueprint('admin', __name__)

from app_histoire.admin import admin_controller
