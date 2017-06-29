from unittest import TestCase
from run import app
from buckeT import db, create_app
from instance.config import app_config
from base64 import b64encode
from flask import current_app, json, url_for
from buckeT.database_models import User, BucketList, BucketListItem

app.config.from_object(app_config["testing"])

class BaseTests(TestCase):
    """Base configurations for the testcases."""

    def setUp(self):
        self.test_client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.URL = '/auth/'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_accept_content_type_headers(self):
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def get_authentication_headers(self, first_name, second_name, email, password):
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = \
        'Basic ' + b64encode((self.test_first_name + ':' + self.test_second_name + ':' + self.test_email + ':' + self.test_password).encode('utf- 8')).decode('utf-8')
        return authentication_headers


























































    #     """create test database and set up test client."""
    #     self.test_app = app.test_client()
    #     db.create_all()
    #     user = User(first_name="user", second_name="name", email="user.name@gmail.com", password="username")

    #     # bucketlist = Bucketlist(title="Travel",
    #     #                         description="Places I have to visit",
    #     #                         created_by=1)

    #     # item = Item(name="Enjoy the beautiful beaches of Hawaii",
    #     #             bucketlist_id=1)

    #     db.session.add(user)
    #     # db.session.add(bucketlist)
    #     # db.session.add(item)
    #     db.session.commit()

    # def tearDown(self):
    #     """Destroy the database."""
    #     db.session.remove()
    #     db.drop_all()