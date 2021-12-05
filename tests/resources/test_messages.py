# import re
# from .view_test import ViewTest
# from faker import Faker
# from tests.models.test_messages import TestMessage

# class TestMessage(ViewTest):
#     """
#         Simulate the user login for testing the resources
#         :return: user
#     """

#     faker = Faker('it_IT')


#     @classmethod
#     def create_and_login(cls):
#         user = TestUser.generate_random_user()
#         cls.user_manager.create_user(user=user)

#         return user

#     def test_create_user(self):
#         user = TestUser.generate_random_user()

#         body = {
#             'email': user.email,
#             'password': user.password,
#             'firstname': user.first_name,
#             'lastname': user.last_name,
#             'date_of_birth': user.date_of_birth,
#             'location': user.location
#         }
#         response = self.client.post('/user', json=body)
#         json_response = response.json

#         assert response.status_code == 201
#         assert json_response["status"] == 'success'
#         assert json_response["message"] == 'Successfully registered'

#     def test_profile(self):
#         fake_id = 999

#         # GET profile: user not found
#         url = '/profile/{}'.format(fake_id)
#         response = self.client.get(url)
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response['status'] == 'User not present'

#         # Change profile information: user not found
#         url = 'profile/{}'.format(fake_id)
#         body = {
#             'email': TestUser.faker.email(),
#             'firstname': TestUser.faker.first_name(),
#             'lastname': TestUser.faker.last_name(),
#             'location': TestUser.faker.city()

#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response["status"] == 'Not found'

#         # Update language filter: user not found
#         url = '/profile/{}/language_filter'.format(fake_id)
#         response = self.client.post(url)
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response["status"] == 'failed'
#         assert json_response["message"] == 'Could not update language filter, user not found'

#         user = self.create_and_login()
#         user.set_profile_pic(TEST_PATH_FILE)

#         # GET profile: user found
#         url = '/profile/{}'.format(user.id)
#         response = self.client.get(url)

#         assert response.status_code == 200

#         # Change profile information with existing email
#         user1 = TestUser.generate_random_user()
#         user1.set_email('test1@test.com')
#         self.user_manager.create_user(user=user1)

#         url = 'profile/{}'.format(user.id)
#         body = {
#             'email': user1.email,
#             'firstname': TestUser.faker.first_name(),
#             'lastname': TestUser.faker.last_name(),
#             'location': TestUser.faker.city()

#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 409
#         assert json_response["status"] == 'not success'
#         assert json_response["message"] == 'Email already exists'

#         # Change profile information with wrong email
#         url = 'profile/{}'.format(user.id)
#         body = {
#             'email': 'wrong@wrong.com',
#             'firstname': TestUser.faker.first_name(),
#             'lastname': TestUser.faker.last_name(),
#             'location': TestUser.faker.city()

#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 409
#         assert json_response["status"] == 'not success'
#         assert json_response["message"] == 'Incorrect email format'

#         # Change profile information
#         url = 'profile/{}'.format(user.id)
#         body = {
#             'email': 'new@test.com',
#             'firstname': TestUser.faker.first_name(),
#             'lastname': TestUser.faker.last_name(),
#             'location': TestUser.faker.city()

#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 200
#         assert json_response["status"] == 'success'
#         assert json_response["message"] == 'Successfully updated'

#         # Update language filter
#         url = '/profile/{}/language_filter'.format(user.id)
#         response = self.client.post(url)
#         json_response = response.json

#         assert response.status_code == 202
#         assert json_response["status"] == 'success'
#         assert json_response["message"] == 'Successfully updated language filter'

#         # Change profile picture unexistent user
#         url = 'profile/{}/profile_picture'.format(fake_id)
#         body = {
#             'format': 'png',
#             'file': TEST_BINARY_FILE
#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response["status"] == 'failed'
#         assert json_response["message"] == 'Could not update the profile picture, user not found'

#         # Change profile picture
#         url = 'profile/{}/profile_picture'.format(user.id)
#         body = {
#             'format': 'png',
#             'file': TEST_BINARY_FILE
#         }
#         response = self.client.post(url, json=body)
#         json_response = response.json

#         assert response.status_code == 202
#         assert json_response["status"] == 'success'
#         assert json_response["message"] == 'Profile picture updated'

#     def test_get_user(self):
#         # GET non existent user by id
#         fake_id = 999
#         response = self.client.get('/user/{}'.format(fake_id))
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response['status'] == 'User not present'

#         # GET user by id
#         user = TestUser.generate_random_user()
#         self.user_manager.create_user(user=user)
#         response = self.client.get('/user/{}'.format(user.id))

#         assert response.status_code == 200

#         # GET non existent user by email
#         fake_email = 'fake@fake.com'
#         response = self.client.get('/user_email/{}'.format(fake_email))
#         json_response = response.json

#         assert response.status_code == 404
#         assert json_response['status'] == 'User not present'

#         # GET user by email
#         response = self.client.get('/user_email/{}'.format(user.email))

#         assert response.status_code == 200

#     def test_users_list(self):
#         # GET users list
#         response = self.client.get('/users/')
#         json_response = response.json

#         assert response.status_code == 200
#         assert json_response['status'] == 'success'