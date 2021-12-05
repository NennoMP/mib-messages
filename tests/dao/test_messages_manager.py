from faker import Faker

from .dao_test import DaoTest


class TestMessageManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestMessageManager, cls).setUpClass()
        from tests.models.test_messages import TestMessage
        cls.test_message = TestMessage
        from mib.dao import message_manager
        cls.message_manager = message_manager.MessageManager

    def test_crud(self):
        for _ in range(0, 10):
            message = self.test_message.generate_random_message()
            #CREATE MESSAGE TEST
            self.message_manager.create(message=message)
            #READ MESSAGE TEST
            message1 = self.message_manager.retrieve_by_id(message.id)
            self.test_message.assertmessageEquals(message1, message)

            message1 = self.message_manager.retrieve_by_id(message.id)
            self.test_message.assertmessageEquals(message1, message)
            #TODO: UPDATE MESSAGE TEST
            #TODO: DELETE MESSAGE TEST

    def test_actions(self):
        message = self.test_message.generate_random_message()
        self.message_manager.create(message=message)
        message1 = self.message_manager.retrieve_by_id(message.id)

        message = self.test_message.generate_random_message()
        self.message_manager.create(message=message)
        self.message_manager.retrieve_by_id(message.id)
        message1 = self.message_manager.retrieve_by_id(message.id)
