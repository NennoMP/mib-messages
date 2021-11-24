from flask import request, jsonify
from sqlalchemy.orm import joinedload
#from mib.dao.user_manager import UserManager
from mib.models.message import Message
import datetime

from werkzeug.security import check_password_hash


def create_message():
    text=request.get_json()['text']
    return text+"ciaonepost",200

def get_message_by_id(message_id=None):
    return "ciaoneget",200

def update_message(message_id=None):
    return "ciaoneput",200     

def delete_message(message_id=None):
    return "ciaonedelete",200     
    
