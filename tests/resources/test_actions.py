from datetime import datetime
from typing import Sequence
from flask import json

from .view_test import ViewTest
from faker import Faker
from tests.models.test_messages import TestMessage


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
        sequence_number = 11

        # Create random message
        message = TestMessage.generate_random_message()

        # Get existing message of another user
        url = f"/message/{message.sender_id}/1"
        response = self.client.get(url)
        assert response.status_code == 404

        # Get not existing message
        url = f"/message/{message.sender_id}/100"
        response = self.client.get(url)
        assert response.status_code == 404

        serialized_message = message.serialize()
        old_date = serialized_message['delivery_date']
        serialized_message['delivery_date'] = datetime.strftime(old_date, '%Y-%m-%d %H:%M:%S')

        # Create message
        response = self.client.post(
            '/message',
            data=json.dumps({'message': serialized_message}),
            content_type='application/json'
        )
        assert response.status_code == 201

        # Get existing message
        response = self.client.get(f'/message/{message.sender_id}/{sequence_number}')
        assert response.status_code == 200

        # Update not existing message (deliver)
        message.is_delivered = True
        message.is_draft = False
        message.text = 'new'
        serialized_message = message.serialize()
        old_date = serialized_message['delivery_date']
        serialized_message['delivery_date'] = datetime.strftime(old_date, '%Y-%m-%d %H:%M:%S')
        response = self.client.put(
            f"/message/{message.sender_id}/100",
            data=json.dumps({'message': serialized_message}),
            content_type='application/json'
        )
        assert response.status_code == 404

        # Update existing message with no rights
        response = self.client.put(
            f"/message/0/{sequence_number}",
            data=json.dumps({'message': serialized_message}),
            content_type='application/json'
        )
        assert response.status_code == 404

        # Update existing message
        response = self.client.put(
            f"/message/{message.sender_id}/{sequence_number}",
            data=json.dumps({'message': serialized_message}),
            content_type='application/json'
        )
        assert response.status_code == 200

        # Read new message
        response = self.client.get(f'/message/{message.recipient_id}/{sequence_number}')
        assert response.status_code == 200

        # Verifing update existing message
        response = self.client.get(f"/message/{message.sender_id}/{sequence_number}")
        assert response.get_json()['text'] == serialized_message['text']

        # Delete not existing message
        response = self.client.delete(f"/message/{message.sender_id}/100")
        assert response.status_code == 404

        # Delete existing message (sender)
        response = self.client.delete(f"/message/{message.sender_id}/{sequence_number}")
        assert response.status_code == 200

        # Delete existing message (recipient)
        response = self.client.delete(f"/message/{message.recipient_id}/{sequence_number}")
        assert response.status_code == 200

        # Delete again message
        response = self.client.delete(f"/message/{message.sender_id}/{sequence_number}")
        assert response.status_code == 404

        # Get mailbox
        response = self.client.get(f"/message/{message.sender_id}/messages")
        # assert
        assert response.status_code == 200
