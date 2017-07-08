from base_test_class import BaseClass
import unittest
from run import app
from instance.config import app_config
import json
from buckeT import create_app, db, bucketlist, api
from buckeT.bucketlist import RegisterUser, LoginUser, Bucketlist, BucketlistItem, SingleBucketlist, SingleBucketlistItem


app.config.from_object(app_config["testing"])

class TestRegisterUser(BaseClass):
    """class holds all tests for registering a user"""
    
    def test_registering_user_with_all_credentials(self):
        """test registering a user"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post('/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 201)
        self.assertTrue(new_data['message'] == 'Sucessfully registered new user!')

    def test_registering_user_with_errors(self):
        """test registering a user with errors in parameters"""

        # error is on the first name parameter
        data = {
            'first_nam': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post('/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 400)
        self.assertTrue(new_data['message'] == 'User not registered due to errors!')

    def test_registering_user_with_none_alphabets_in_names(self):
        """test registering a user with special characters in names"""

        # special character is on the first name parameter
        data = {
            'first_name': '#user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post('/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        print new_data
        self.assertTrue(response.status_code == 409)

    def test_registering_user_who_already_exists(self):
        """test registering a user who already exists"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        self.test_client.post('/auth/register/', data=data)
        response2 = self.test_client.post('auth/register/', data=data)
        new_data2 = json.loads(response2.data.decode('utf-8'))
        self.assertTrue(response2.status_code == 409)
        self.assertTrue(new_data2['message'] == 'User you are entering already exists!')
