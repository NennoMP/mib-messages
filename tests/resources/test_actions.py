from .view_test import ViewTest
from faker import Faker
#from tests.models.test_messages import TestMessage


class TestActions(ViewTest):
    """
        Simulate the user login for testing the resources
        :return: user
    """

    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestActions, cls).setUpClass()

    def test_message(self):

        # Create random message
        message = self.test_message.generate_random_message()
        
        # Get not existing message
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.status_code == 404

        # Create message
        url = "/message"
        response = self.client.post(url, data={'message':message})
        assert response.status_code == 201

        # Get existing message
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.status_code == 200

        #Update not existing message
        message.text='new'
        url = f"/message/{message.sender_id}/100"
        response = self.client.put(url, data={'message':message})
        assert response.status_code == 404

        #Update existing message
        message.text='new'
        url = f"/message/{message.sender_id}/1"
        response = self.client.put(url, data={'message':message})
        assert response.status_code == 200

        #Verifing update existing message
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.get_json()['text'] == message.text

        #Delete not existing message
        url = f"/message/{message.sender_id}/100"
        response = self.client.delete(url)
        assert response.status_code == 404

        #Delete existing message
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.status_code == 200

        #Delete again message
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.status_code == 404







        
