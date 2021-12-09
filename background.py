from datetime import datetime
import os, smtplib, ssl, time
import config

from celery import Celery

from access import Access


import os
os.environ['FLASK_ENV']='development'
os.environ['TZ'] = 'Europe/Rome'
time.tzset()


BACKEND = BROKER = 'redis://localhost:6381/0'

celery = Celery(__name__, broker=BROKER)

_APP = None

from mib import create_app

def lazy_init():
    '''Returns the application singleton.'''
    global _APP
    if _APP is None:
        app = create_app()
        from mib import db
        db.init_app(app)
        _APP = app
    return _APP


def send_email(email, message):
    '''Utility function to send email notification for the application.'''
    password = None
    with open('token.txt') as f:
        password = f.readline()

    smtp_server = 'smtp.gmail.com'
    port = 465
    sender_email = 'asesquad5@gmail.com'
    receiver_email = email
    message = f'''\
    Subject: MyMessageInABottle - Notification

    {message}'''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port,context=context) as server:
        #server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@celery.task
def send_messages():
    '''Reads from the DB all the pending messages with expired delivery date,
       and makes them available for the recipient.
    '''
    app = lazy_init()
    with app.app_context():
        from mib import db
        from mib.models.message import Message
        print(datetime.now())
        messages = db.session.query(Message).filter(
            ~Message.is_delivered,
            ~Message.is_draft,
            Message.delivery_date <= datetime.now(),
            Message.access.op('&')(Access.SENDER.value)  # Message not deleted with the bonus.
        )

        for message in messages:
            message.is_delivered = True
            db.session.commit()
            # Send notification to the recipient.
            notify.delay(message.recipient_id, 'You received a new message!')
            return 'Delivered'

    #return 'Delivered'


@celery.task
def notify(user_id, message):
    '''Sends an email containing <message> to the user
       identified with <user_id>, if present and active.
    '''
    app = lazy_init()
    with app.app_context():
        from mib.rao.user_manager import UserManager
        try: user = UserManager.get_profile_by_id(user_id)
        except RuntimeError as e:
            print(str(e))
            return 
        if user is None or not user['is_active']:
            return 'Email not sent'

        send_email(user['email'], message)
        print(user['email'])
    return 'Email sent'


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''Registers the periodic tasks.'''
    seconds_in_a = {
        'minute': 1,
        'month': 60*60*24*30
    }

    # Send pending messages every 5 minutes.
    sender.add_periodic_task(5 * seconds_in_a['minute'], send_messages.s(), name='send_messages')
