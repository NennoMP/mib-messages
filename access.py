from enum import Enum


class Access(Enum):
    '''Access rights for a message. Unix-style.'''
    NONE      = 0
    SENDER    = 1
    RECIPIENT = 2
    ALL       = 3

    @staticmethod
    def is_sender_or_recipient(message, user_id):
        '''Utility function for checking if the current user
        is allowed to read the message.
        '''
        is_sender = message.sender_id == user_id
        is_recipient = message.recipient_id == user_id

        '''The recipient can access the message if:
        - it has the access rights for the message, and
        - the message is not a draft, and
        - the message is delivered or the recipient is the sender.
        '''
        recipient_authorized = (
            message.access & Access.RECIPIENT.value
            and not message.is_draft
            and (message.is_delivered or is_sender)
        )

        if (not (is_sender or is_recipient)
            or (is_sender and not message.access & Access.SENDER.value)
            or (is_recipient and not recipient_authorized)
        ):
            return False
        return True
