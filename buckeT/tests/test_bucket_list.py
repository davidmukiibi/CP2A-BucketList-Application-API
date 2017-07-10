from base_test_class import BaseClass
import unittest
from run import app
from instance.config import app_config
import json
from buckeT import create_app, db, bucketlist, api
from buckeT.bucketlist import RegisterUser, LoginUser, Bucketlist, BucketlistItem, SingleBucketlist, SingleBucketlistItem

app.config.from_object(app_config["testing"])

class TestBucketList(BaseClass):
    """testing that creation of a bucket list works when all
        required fields are given.
    """

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""

        response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(response.status_code == 201)
 
    def test_bucketlist_creation_with_special_characters(self):
        """Test API can create a bucketlist (POST request)"""

        faulty_bucketlist = {'name': '#jamaica'}
        response = self.test_client.post(self.url_prefix + '/bucketlists/', data=faulty_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(response.status_code == 400)

    def test_create_bucket_list_with_no_name(self):
        """testing that creating a new bucket list with no name doesnt work"""

        bucketlist1 = {'name': ''}
        response = self.test_client.post(self.url_prefix + '/bucketlists/', data=bucketlist1,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(response.status_code == 400)
        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(new_data['message'] == 'Please provide a name for the bucket list.')
        
    def test_create_bucket_list_that_already_exists(self):
        """testing that creating a bucket list that exists doesnt work"""

        response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertTrue(response.status_code == 201)
        response2 = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        new_data = json.loads(response2.data.encode('utf-8'))
        self.assertTrue('Bucket list already exists!' == new_data['message'])
        self.assertTrue(response2.status_code == 409)

    def test_delete_bucket_list(self):
        """testing that a given bucket list can be deleted."""

        self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        response = self.test_client.delete(self.url_prefix + '/bucketlists/1', headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(response.status_code, 200)

        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(new_data['message'] == 'Bucketlist deleted successfully')


    def test_delete_bucket_list_that_doesnt_exist(self):
        """Testing deletion of a bucket list that doesnt exist"""

        response = self.test_client.delete(self.url_prefix + '/bucketlists/1', headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(response.status_code, 404)

        new_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(new_data['message'] == 'No bucket list found with that ID')


    def test_edit_bucket_list(self):
        """testing that the given bucket list can be edited."""
        
        data2 = {'name': 'going to goa'}
        post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(post_response.status_code, 201)
        put_response = self.test_client.put(self.url_prefix + '/bucketlists/1', data=data2,
                                headers={"Authorization": 'Bearer ' + self.token})
        put_data = json.loads(put_response.data.decode('utf-8'))
        self.assertEqual(put_response.status_code, 201)
        self.assertTrue(put_data['message'] == 'Bucket list edit successful')

    def test_edit_bucket_list_that_doesnt_exist(self):
        """testing editing a bucket list that doesnt exist"""

        data2 = {'name': 'going to goa'}
        put_response = self.test_client.put(self.url_prefix + '/bucketlists/1', data=data2,
                                headers={"Authorization": 'Bearer ' + self.token})
        put_data = json.loads(put_response.data.decode('utf-8'))
        self.assertEqual(put_response.status_code, 404)
        self.assertTrue(put_data['message'] == 'No bucket list found with that ID')

    def test_edit_bucket_list_with_no_name(self):
        
        data2 = {'name': ''}
        post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(post_response.status_code, 201)
        put_response = self.test_client.put(self.url_prefix + '/bucketlists/1', data=data2,
                                headers={"Authorization": 'Bearer ' + self.token})
        put_data = json.loads(put_response.data.decode('utf-8'))
        self.assertEqual(put_response.status_code, 400)
        self.assertTrue(put_data['message'] == 'Please enter a name to replace the current one stored!')
    


    def test_fetching_a_bucket_list_by_id(self):
        """testing that fetching a bucket list by id from the database works."""

        post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        get_response = self.test_client.get(self.url_prefix + '/bucketlists/1',
                                headers={"Authorization": 'Bearer ' + self.token})
        get_data = json.loads(get_response.data.decode('utf-8'))
        self.assertTrue(get_response.status_code, 200)
        self.assertTrue('go to jamaica once again!' in get_data[0]['bucket list']['name'])


    def test_fetching_a_bucket_list_by_none_existant_id(self):
        """Fetching a bucket list that doesnt exist"""

        get_response = self.test_client.get(self.url_prefix + '/bucketlists/1',
                                headers={"Authorization": 'Bearer ' + self.token})
        get_data = json.loads(get_response.data.decode('utf-8'))
        self.assertTrue(get_response.status_code, 404)
        self.assertTrue('No bucket list with that given ID.' == get_data['message'])

    def test_fetching_bucket_lists(self):
        """Test API can get a bucketlist (GET request)."""
        post_response = self.test_client.post(self.url_prefix + '/bucketlists/', data=self.new_bucketlist,
                                 headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(post_response.status_code, 201)
        get_response = self.test_client.get(self.url_prefix + '/bucketlists/',
                                headers={"Authorization": 'Bearer ' + self.token})
        self.assertEqual(get_response.status_code, 200)


    def test_fetching_bucketlists_without_logging_in(self):
        get_response = self.test_client.get(self.url_prefix + '/bucketlists/1',
                                headers={"Authorization": ''})
        get_data = json.loads(get_response.data.decode('utf-8'))
        self.assertTrue(get_response.status_code, 401)

