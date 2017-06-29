from flask import json, url_for
import simplejson as json
from buckeT import app
# from flask_api import FlaskAPI
from buckeT import create_app, db
from base_test_class import BaseTests
from buckeT import bucketlist
from buckeT.database_models import User, BucketList, BucketListItem

class TestRegisterUser(BaseTests):

    def test_registering_user_with_all_credentials(self):
        """test registering a user"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        response = self.test_client.post(self.URL + 'register/', data=data)
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
        response = self.test_client.post(self.URL + 'register/', data=data)
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
        response = self.test_client.post(self.URL + 'register/', data=data)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 409)
        self.assertTrue(new_data['message'] == 'first name or second name can not contain special characters or numbers!')

    def test_registering_user_who_already_exists(self):
        """test registering a user who already exists"""
        data = {
            'first_name': 'user',
            'second_name': 'name',
            'email': 'user.name@gmail.com',
            'password': 'userpassword'
        }
        self.test_client.post(self.URL + 'register/', data=data)
        response2 = self.test_client.post(self.URL + 'register/', data=data)
        new_data2 = json.loads(response2.data.decode('utf-8'))
        self.assertTrue(response2.status_code == 409)
        self.assertTrue(new_data2['message'] == 'User you are entering already exists!')


   # def test_remove_a_registered_user(self):
    #     """testing that a user can be removed from the system."""
    #     pass
    # def test_remove_an_unregistred_user(self):
    #     """testing that removing an unregistered user from the system isnt possible."""
    #     pass






# make tests executable
# if __name__ == '__main__':
#     unittest.main()
