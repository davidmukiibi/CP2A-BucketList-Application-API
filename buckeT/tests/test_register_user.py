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
        response = self.test_client.post(self.url_prefix + '/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 201)
        self.assertTrue(new_data['message'] == 'Successfully registered new user!')

    def test_registering_user_without_some_fields(self):
        """test registering a user with errors in parameters"""

        # error is on the first name variable
        data = {
            'first_name': '',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post(self.url_prefix + '/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 400)
        self.assertTrue(new_data['message'] == 'First name should not be empty!')

    def test_registering_user_with_none_alphabets_in_names(self):
        """test registering a user with special characters in names"""

        # special character is on the first name parameter
        data = {
            'first_name': '#user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post(self.url_prefix + '/auth/register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 400)

    def test_registering_user_who_already_exists(self):
        """test registering a user who already exists"""

        self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        response2 = self.test_client.post(self.url_prefix + '/auth/register/', data=self.registration_payload)
        new_data2 = json.loads(response2.data.decode('utf-8'))
        self.assertTrue(response2.status_code == 409)
        self.assertTrue(new_data2['message'] == 'User you are entering already exists!')

    def test_password_length(self):
        """testing the length of the password entered"""
        
        new_user = {
                        'first_name': 'david',
                        'second_name': 'mukiibi',
                        'email': 'david.mukiibi@gmail.com',
                        'password': '123456'
                    }
        get_response = self.test_client.post(self.url_prefix + '/auth/register/', data=new_user)
        get_data = json.loads(get_response.data.decode('utf-8'))

        self.assertTrue(get_response.status_code, 400)
        self.assertTrue(get_data['message'] == 'Password should be longer than 8 characters!')

    def test_email_validation(self):
        """Testing email validation"""
        
        new_user = {
                        'first_name': 'david',
                        'second_name': 'mukiibi',
                        'email': 'davidmukiibigmail',
                        'password': '123456'
                    }
        post_response = self.test_client.post(self.url_prefix + '/auth/register/', data=new_user)
        self.assertTrue(post_response.status_code, 400)
