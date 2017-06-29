from flask import json, url_for
import simplejson as json
from buckeT import app
# from flask_api import FlaskAPI
from buckeT import create_app, db
from base_test_class import BaseTests
from buckeT import bucketlist
from buckeT.database_models import User, BucketList, BucketListItem

class TestLoginUser(BaseTests):

    def test_logging_in_user_with_correct_credentials(self):
        """test loggin in a user with correct credentials"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        data2 = {
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response = self.test_client.post(self.URL + 'login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(new_data['message'] == 'Successfully logged in')

    def test_logging_in_user_with_incorrect_credentials(self):
        """test logging in user with wrong credentials"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        data2 = {
            'email': 'er.name@gmail.com',
            'password': 'userpassword'
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response = self.test_client.post(self.URL + 'login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 401)
        self.assertTrue(new_data['message'] == 'User does not exist!')

    def test_logging_in_user_without_password(self):
        """test logging in user with missing password"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        data2 = {
            'email': 'user.name@gmail.com',
            'password': ''
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response = self.test_client.post(self.URL + 'login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 401)
        self.assertTrue(new_data['message'] == 'Wrong password!')


    def test_logging_in_user_without_email(self):
        """test logging in user with missing email"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        data2 = {
            'email': '',
            'password': 'userpassword'
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response = self.test_client.post(self.URL + 'login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 401)
        self.assertTrue(new_data['message'] == 'User does not exist!')

    def test_logging_in_user_who_doesnt_exist(self):
        """test logging in user who doesnt exist"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        data2 = {
            'email': 'user2.name@gmail.com',
            'password': 'password3'
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response = self.test_client.post(self.URL + 'login/', data=data2)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 401)
        self.assertTrue(new_data['message'] == 'User does not exist!')
