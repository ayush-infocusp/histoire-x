from flask import Blueprint

bp = Blueprint('client', __name__)

from app_histoire.client import client_controller
