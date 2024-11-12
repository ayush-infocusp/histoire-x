from flask import Blueprint

bp = Blueprint('main', __name__)

from app_histoire.main import auth_contoller
