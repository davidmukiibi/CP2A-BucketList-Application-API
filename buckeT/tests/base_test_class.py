import unittest
from buckeT import app
from instance.config import app_config
import json
from buckeT import create_app, db, bucketlist, api
from buckeT.bucketlist import RegisterUser, LoginUser, Bucketlist, BucketlistItem, SingleBucketlist, SingleBucketlistItem

app.config.from_object(app_config["testing"])

class BaseClass(unittest.TestCase):
    """Parent class to hold the setup and teardown methods"""

    def setUp(self):
        """setting up test dependencies"""

        self.test_client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # creating testing db tables
        db.create_all()

        # user credentials for registering user
        self.registration_payload = {
                        'first_name': 'david',
                        'second_name': 'mukiibi',
                        'email': 'david.mukiibi@yahoo.com',
                        'password': '12345678902'
                    }

        # user credentials for logging in user
        self.login_payload = {'email': 'david.mukiibi@yahoo.com',
                        'password': '12345678902'
                    }
        self.url_prefix = '/api/v1'

        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        login_instance = self.test_client.post(self.url_prefix + '/auth/login/', data=self.login_payload)
        response = json.loads(login_instance.data.decode('utf-8'))
        self.token = response['token']['access_token']

        # creating a bucketlist
        self.new_bucketlist = {'name': 'go to jamaica once again!'}

        # Bucketlist item details for item creation
        self.new_bucketlist_item = {'name': 'book a flight'}


    def tearDown(self):
        """tearing down the dependencies"""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()