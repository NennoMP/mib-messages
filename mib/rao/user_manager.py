import requests
from flask import abort

from mib import app


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_profile_by_id(cls, user_id):
        """
        This method contacts the users microservice
        and retrieves the user profile by user id.
        :param user_id: the user id
        :return: dictionary with user data
        """
        try:
            response = requests.get("%s/profile/%s" % (cls.USERS_ENDPOINT, str(user_id)),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                return json_payload
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise RuntimeError(
                    f'Error connecting to {cls.USERS_ENDPOINT}')
