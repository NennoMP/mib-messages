import os
from better_profanity import profanity
from copy import copy
from datetime import datetime
from flask import request, jsonify
from functools import wraps

from mib.dao.message_manager import MessageManager
from mib.rao.user_manager import UserManager
from mib.models import Message
from access import Access


env = os.getenv('FLASK_ENV', 'None')

if env != 'testing':
    from background import notify


def check_none_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            MessageManager.check_none(**kwargs)
        except ValueError:
            return 'Missing user_id or message_id', 400
        return func(*args, **kwargs)
    return wrapper


def filter_language(message):
    '''Utility function for censoring bad language in received messages.'''
    message.text = profanity.censor(message.text)


def create_message():
    ''''Allows to create a new message.'''
    json_message = request.get_json()['message']
    json_message['delivery_date'] = datetime.strptime(json_message['delivery_date'], '%Y-%m-%d %H:%M:%S')
    message = Message(**json_message)
    MessageManager.create(message=message)
    return 'Message created', 201


@check_none_args
def get_message_by_id(user_id=None, message_id=None):
    '''Allows the user to read a specific message by id.

       GET: display the content of a specific message by id (censored if language_filter is ON)
    '''
    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404

    if message.recipient_id == user_id and not message.is_draft and not message.is_read and message.is_delivered:
        if env != 'testing':
            notify.delay(message.sender_id, 'Your message has been read!')
        message.is_read = True
        MessageManager.update()

    message_aux = copy(message)
    if user_id == message.recipient_id:
        try:
            current_user = UserManager.get_profile_by_id(user_id)
            if current_user['has_language_filter']:
                filter_language(message_aux)
        except RuntimeError:
            message_aux.text = ''

    return jsonify(message_aux.serialize()), 200


@check_none_args
def update_message(user_id=None, message_id=None):
    ''''Allows to update a message.'''
    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404
        
    json_message = request.get_json()['message']

    message.text = json_message['text']
    message.is_draft = json_message['is_draft']
    message.recipient_id = json_message['recipient_id']
    if 'is_delivered' in json_message:
        message.is_delivered = json_message['is_delivered']
    if 'delivery_date' in json_message:
        message.delivery_date = datetime.strptime(json_message['delivery_date'], '%Y-%m-%d %H:%M:%S')
    MessageManager.update()
    return 'Message updated', 200


@check_none_args
def delete_message(user_id=None, message_id=None):
    '''Allows the user to delete a specific message by id.'''
    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404

    # Delete scheduled message using bonus
    if not message.is_draft and not message.is_delivered:
        message.access -= Access.SENDER.value
        MessageManager.update()
        return jsonify({'msg': 'Message deleted successfully'}), 200

    # DELETE for the point of view of the current user.
    if message.sender_id == user_id:
        message.access -= Access.SENDER.value
    if message.recipient_id == user_id:
        message.access -= Access.RECIPIENT.value
    MessageManager.update()
    message='<h3>Message deleted!</h3><br/>'
    return jsonify({'msg': 'Message deleted successfully'}), 200


@check_none_args
def get_messages(user_id=None):
    '''Retrieves sent, received and draft messages of a user by their id'''    
    
    # Retrieve sent messages of user <id>
    sent_messages = MessageManager.retrieve_by_type(user_id, 'sent')

    # Retrieve received messages of user <id>
    received_messages = MessageManager.retrieve_by_type(user_id, 'received')

    # Retrieve draft messages of user <id>
    draft_messages = MessageManager.retrieve_by_type(user_id, 'draft')

    # Retrieve scheduled messages of user <id>
    scheduled_messages = MessageManager.retrieve_by_type(user_id, 'scheduled')

    return jsonify({
        'sent':     [message.serialize() for message in sent_messages],
        'received': [message.serialize() for message in received_messages],
        'drafts':   [message.serialize() for message in draft_messages],
        'scheduled': [message.serialize() for message in scheduled_messages]
    }), 200
