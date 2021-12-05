from mib import db
from mib.models import Message
from access import Access


class MessageManager(object):
    db_session = db.session

    @staticmethod
    def check_none(**kwargs):
        for name, arg in zip(kwargs.keys(), kwargs.values()):  #TODO_ check name, arg in kwargs.items():
            if arg is None:
                raise ValueError(f'You can\'t set {name} argument to None')


    @staticmethod
    def retrieve_by_id(message_id):
        message = db.session.query(Message).filter(Message.id == message_id).first()
        if message is None:
            raise KeyError
        return message


    @staticmethod
    def retrieve_by_type(user_id, type):
        condition = {
            'sent': (
                Message.sender_id == user_id,
                Message.access.op('&')(Access.SENDER.value),
                ~Message.is_draft,
                Message.is_delivered
            ),
        
            'received': (
                Message.recipient_id == user_id,
                Message.access.op('&')(Access.RECIPIENT.value),
                Message.is_delivered
            ),

            'draft': (
                Message.sender_id == user_id,
                Message.access.op('&')(Access.SENDER.value),
                Message.is_draft
            )
        }

        return db.session.query(Message).filter(*condition[type]).all()


    @staticmethod
    def create(**kwargs):
        for bean in kwargs.values():
            db.session.add(bean)
        db.session.commit()


    @staticmethod
    def update():
        db.session.commit()
