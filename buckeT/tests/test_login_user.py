from base_test_class import BaseClass
import unittest
from run import app
from instance.config import app_config
import json
from buckeT import create_app, db, bucketlist, api
from buckeT.bucketlist import RegisterUser, LoginUser, Bucketlist, BucketlistItem, SingleBucketlist, SingleBucketlistItem

app.config.from_object(app_config["testing"])

class TestLoginUser(BaseClass):
    """class holds all tests for logging in a user."""

    def test_logging_in_user_with_correct_credentials(self):
        """test logging in a user with correct credentials"""

        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response = self.test_client.post(self.url_prefix + '/auth/login/', data=self.login_payload)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 201)
        self.assertTrue(new_data['message'] == 'Successfully logged in')

    def test_logging_in_user_with_incorrect_credentials(self):
        """test logging in user with wrong credentials"""
        data2 = {
            'email': 'er.name@gmail.com',
            'password': 'userpassword'
        }
        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response = self.test_client.post(self.url_prefix + '/auth/login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 404)
        self.assertTrue(new_data['message'] == 'User does not exist!')

    def test_logging_in_user_without_password(self):
        """test logging in user with missing password"""
        data2 = {
            'email': 'david.mukiibi@yahoo.com',
            'password': ''
        }
        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response = self.test_client.post(self.url_prefix + '/auth/login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 400)
        self.assertTrue(new_data['message'] == 'Wrong password!')


    def test_logging_in_user_without_email(self):
        """test logging in user with missing email"""
        data2 = {
            'email': '',
            'password': 'userpassword'
        }
        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response = self.test_client.post(self.url_prefix + '/auth/login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 404)
        self.assertTrue(new_data['message'] == 'User does not exist!')

    def test_logging_in_user_who_doesnt_exist(self):
        """test logging in user who doesnt exist"""
        data2 = {
            'email': 'user2.name@gmail.com',
            'password': 'password3'
        }
        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response = self.test_client.post(self.url_prefix + '/auth/login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 404)
        self.assertTrue(new_data['message'] == 'User does not exist!')



