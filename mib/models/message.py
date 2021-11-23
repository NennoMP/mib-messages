from werkzeug.security import generate_password_hash, check_password_hash

from mib import db

class Message(db.Model):
    """Representation of Message model."""

    # The name of the table that we explicitly set
    __tablename__ = 'Message'

    # A list of fields to be serialized
    #SERIALIZE_LIST = ['id', 'sender_id', 'recipient_id', 'text', 'delivery_date', 'access']

    # Data
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Unicode(128),nullable=False)
    delivery_date = db.Column(db.DateTime)
    access = db.Column(db.Integer, default=Access.ALL.value)    # Access rights.
    # Booleans
    is_draft = db.Column(db.Boolean, default=True)
    is_delivered = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    # Files (path)
    attachment = db.Column(db.String, default=None)    # Attachments

    # Relationships to 'User' table
    sender = relationship('User', foreign_keys='Message.sender_id')
    recipient = relationship('User', foreign_keys='Message.recipient_id')

    def __init__(self, *args, **kw):
        super(Message, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def get_sender(self):
        return self.sender_id

    def get_recipient(self):
        return self.recipient_id

    def get_text(self):
        return self.text

    def get_delivery_date(self):
        return self.delivery_date

    def get_attachement(self):
        return self.attachment