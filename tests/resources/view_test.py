import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from mib import create_app
        app = create_app()
        cls.client = app.test_client()

        from tests.models.test_messages import TestMessage
        cls.test_user = TestMessage

        from mib.dao.message_manager import MessageManager
        cls.user_manager = MessageManager  
