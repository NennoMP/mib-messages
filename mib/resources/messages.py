from better_profanity import profanity
from flask import request, jsonify

from mib.dao.message_manager import MessageManager
from mib.models import Message
from access import Access

from werkzeug.security import check_password_hash


def filter_language(message):
    '''Utility function for censoring bad language in received messages.'''
    return {
        'text': profanity.censor(message.text),  # Censorship.
        'delivery_date': message.delivery_date,
        'recipient_id': message.recipient_id,
        'sender': message.sender,
        'recipient': message.recipient,
        'is_draft': message.is_draft,
        'is_delivered': message.is_delivered
    }


def create_message():
    ''''Allows to create a new message.'''
    json_message = request.get_json()['message']
    message = Message(**json_message)
    MessageManager.create(message=message)
    return 'Message created', 201


def get_message_by_id(user_id=None, message_id=None):
    '''Allows the user to read a specific message by id.

       GET: display the content of a specific message by id (censored if language_filter is ON)
    '''
    if user_id is None or message_id is None:
        return 'TODO', 404

    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404

    if message.get_recipient() == user_id and not message.is_draft and not message.is_read and message.is_delivered:
        #notify.delay(message.get_sender(), 'Your message has been read!')
        message.is_read = True
        MessageManager.update()

    message_aux = message
    #if current_user.has_language_filter:  # TODO: call user microservice
    #    message_aux = filter_language(message)

    return jsonify(message_aux.serialize()), 200


def update_message(user_id=None, message_id=None):
    ''''Allows to update a message.'''
    if user_id is None or message_id is None:
        return 'TODO', 404

    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404
        
    json_message = request.get_json()['message']

    message.text = json_message['text']
    if 'delivery_date' in json_message:
        message.delivery_date = json_message['delivery_date']
    MessageManager.update()
    return 'Message updated', 200


# TODO: decorator for sanity and access checks.
def delete_message(user_id=None, message_id=None):
    '''Allows the user to delete a specific message by id.'''
    if user_id is None or message_id is None:
        return 'TODO', 404

    try:
        message = MessageManager.retrieve_by_id(message_id)
    except KeyError:
        return 'Message not found', 404

    if not Access.is_sender_or_recipient(message, user_id):
        return 'Message not found', 404

    # Delete scheduled message using bonus

    # TODO: check user bonus
    if not message.is_draft and not message.is_delivered: # and current_user.bonus > 0:
        #user = db.session.query(User).filter(User.id==user_id).first()
        #user.bonus -= 1
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


def get_messages(user_id=None):
    '''Retrieves sent, received and draft messages of a user by their id'''
    if user_id is None:
        return 'User not found', 404
    
    # Retrieve sent messages of user <id>
    sent_messages = MessageManager.retrieve_by_type(user_id, 'sent')

    # Retrieve received messages of user <id>
    received_messages = MessageManager.retrieve_by_type(user_id, 'received')

    # Retrieve draft messages of user <id>
    draft_messages = MessageManager.retrieve_by_type(user_id, 'draft')

    return jsonify({
        'sent':     [message.serialize() for message in sent_messages],
        'received': [message.serialize() for message in received_messages],
        'drafts':   [message.serialize() for message in draft_messages]
    }), 200
