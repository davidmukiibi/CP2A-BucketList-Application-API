from base_test_class import BaseClass
import unittest
from run import app
from instance.config import app_config
import json
from buckeT import create_app, db, bucketlist, api
from buckeT.bucketlist import RegisterUser, LoginUser, Bucketlist, BucketlistItem, SingleBucketlist, SingleBucketlistItem

app.config.from_object(app_config["testing"])

class TestBucketListItem(BaseClass):
    """testing that creation of a bucket list Item works given all
        required fields are given.
    """

    def test_create_bucket_list_item(self):
        """testing that creating a bucket list item works with the requiered details given."""

        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)

        new_data = json.loads(bucketlist_item_response.data.decode('utf-8'))
        self.assertTrue('Item saved successfully.' == new_data['message'])


    def test_create_bucket_list_item_with_missing_name(self):
        """testing that creating a bucket list item with no name doesnt work"""

        faulty_buckelist_item = {'name': ''}
        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=faulty_buckelist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 400)

        new_data = json.loads(bucketlist_item_response.data.decode('utf-8'))
        self.assertTrue('Please provide an item name' == new_data['message'])


    def test_create_bucket_list_item_on_non_existant_bucket_list(self):
        """testing that creating a bucket list item on bucket list
        that doesnt exist, does not work
        """

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 404)

        new_data = json.loads(bucketlist_item_response.data.decode('utf-8'))
        self.assertTrue('Bucket list you are trying to add to does not exist' == new_data['message'])

    def test_edit_bucket_list_item(self):
        """testing that a bucket list item can be edited."""

        bucketlist_item_edits = {'name': 'go to uganda first'}
        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)

        bucketlist_item_edit_response = self.test_client.put(self.url_prefix + '/bucketlists/1/items/1', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_edit_response.status_code == 201)

        new_data = json.loads(bucketlist_item_edit_response.data.decode('utf-8'))
        self.assertTrue('Item edited successfully.' == new_data['message'])


    def test_edit_bucket_list_item_with_no_name(self):
        """testing editing bucket list with no name given."""

        bucketlist_item_edits = {'name': ''}
        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)

        bucketlist_item_edit_response = self.test_client.put(self.url_prefix + '/bucketlists/1/items/1', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_edit_response.status_code == 400)

        new_data = json.loads(bucketlist_item_edit_response.data.decode('utf-8'))
        self.assertTrue('Please provide an item name.' == new_data['message'])

    def test_edit_bucket_list_item_which_doesnt_exit(self):
        """testing editing bucketlist item that does not exist."""

        bucketlist_item_edits = {'name': 'go some place'}
        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)

        bucketlist_item_edit_response = self.test_client.put(self.url_prefix + '/bucketlists/1/items/2', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_edit_response.status_code == 404)

        new_data = json.loads(bucketlist_item_edit_response.data.decode('utf-8'))
        self.assertTrue('No item with the given ID!' == new_data['message'])

    def test_edit_bucket_list_item_on_bucketlist_that_doesnt_exist(self):
        """testing editing item on non existent bucketlist."""

        bucketlist_item_edits = {'name': 'go some place'}
        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)

        bucketlist_item_edit_response = self.test_client.put(self.url_prefix + '/bucketlists/2/items/2', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_edit_response.status_code == 404)

        new_data = json.loads(bucketlist_item_edit_response.data.decode('utf-8'))
        self.assertTrue('Bucket list with that ID doesnt exist!' == new_data['message'])


    def test_delete_a_bucket_list_item(self):
        """tesing that a bucketlist item can be deleted."""

        bucketlist_item_edits = {'name': 'go some place'}
        bucketlist_post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_post_response.status_code == 201)
        bucketlist_item_post_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_post_response.status_code == 201)
        bucketlist_item_post_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_post_response.status_code == 201)
        bucketlist_item_delete_response = self.test_client.delete(self.url_prefix + '/bucketlists/1/items/1',
                                headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_delete_response.status_code == 200)
        bucketlist_item_edit_response = self.test_client.put(self.url_prefix + '/bucketlists/2/items/1', data=bucketlist_item_edits,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_edit_response.status_code == 404)


    def test_delete_a_bucket_list_item_that_doesnt_exist(self):
        """tesing deleting of a bucketlist item that does not exist."""

        bucketlist_post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_post_response.status_code == 201)
        bucketlist_item_post_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_post_response.status_code == 201)
        bucketlist_item_delete_response = self.test_client.delete(self.url_prefix + '/bucketlists/1/items/2',
                                headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_delete_response.status_code == 404)

    def test_adding_item_that_already_exists(self):
        """testing that adding an item that already exists doesnt happen"""

        bucketlist_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_response.status_code == 201)

        bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(bucketlist_item_response.status_code == 201)
        another_bucketlist_item_response = self.test_client.post(self.url_prefix + '/bucketlists/1/items/', data=self.new_bucketlist_item,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(another_bucketlist_item_response.status_code == 409)

        new_data = json.loads(another_bucketlist_item_response.data.decode('utf-8'))
        self.assertTrue('The item you are trying to add already exists!' == new_data['message'])