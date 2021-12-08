import unittest
from datetime import datetime

from faker import Faker

from .model_test import ModelTest


class TestMessage(ModelTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestMessage, cls).setUpClass()

        from mib.models import message
        cls.message = message

    @staticmethod
    def assertmessageEquals(value, expected):
        t = unittest.FunctionTestCase(TestMessage)
        t.assertEqual(value.sender_id, expected.sender_id)
        t.assertEqual(value.recipient_id, expected.recipient_id)
        t.assertEqual(value.text, expected.text)
        t.assertEqual(value.delivery_date, expected.delivery_date)
        t.assertEqual(value.is_delivered, expected.is_delivered)

    
    def generate_random_message():
        from mib.models import Message

        sender_id = TestMessage.faker.random_number()
        recipient_id = TestMessage.faker.random_number()
        text = TestMessage.faker.text()
        delivery_date = datetime.now().replace(microsecond=0)
        # Booleans
        is_draft = True
        is_delivered = False
        is_read = False

        message = Message(
            sender_id = sender_id,
            recipient_id = recipient_id,
            text = text,
            delivery_date = delivery_date,
            is_draft = is_draft,
            is_delivered = is_delivered,
            is_read = is_read
        )

        return message
