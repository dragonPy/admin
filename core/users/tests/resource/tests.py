import datetime,json
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from users.models import UserAccessToken, User
from users.api.resources import UserAccessKeyResource, UserResource


class UserResourceTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(UserResourceTest, self).setUp()
        self.list_endpoint = '/api/v1/%s/'
        self.resource_name = 'user'
        self.resource_list_endpoint = self.list_endpoint % self.resource_name
        self.resource_pk = 'id'
        self.detail_url = self.resource_list_endpoint + '{0}/'

        self.post_data_wrong = {
            'username': '22xxx22333',
            # 'mobile': '17721070527',
            'user_pass': 'j;lkj;aksdflkllkj',
        }

        self.post_data = {
            'username': '22xxx22333',
            'email': 'aa@aa.com',
            'user_pass': 'j;lkj;aksdflkllkj'
        }

    def get_credentials(self):
        return UserResource 

    def post(self, data):
        return self.api_client.post(
            self.resource_list_endpoint, 
            format='json', 
            data=data, 
            authentication=self.get_credentials()
        )

    def test_post_list_unauthorized(self):
        self.assertEqual(User.objects.count(), 0)
        resp = self.post(self.post_data_wrong)
        # print resp
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), 0)

    def test_post_list(self):
        self.assertEqual(User.objects.count(), 0)
        resp = self.post(self.post_data)
        # print resp
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), 1)

class UserAccessKeyResourceTest(ResourceTestCaseMixin, TestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    # fixtures = ['test_entries.json']

    def setUp(self):
        super(UserAccessKeyResourceTest, self).setUp()
        self.list_endpoint = '/api/v1/%s/'
        self.resource_name = 'useraccesskey'
        self.resource_list_endpoint = self.list_endpoint % self.resource_name
        self.resource_pk = 'access_key'
        self.detail_url = self.resource_list_endpoint + '{0}/'

        self.post_data = {
            'user_id': '1'
        }

    def get_credentials(self):
        return UserAccessKeyResource 

    def post(self):
        return self.api_client.post(
            self.resource_list_endpoint, 
            format='json', 
            data=self.post_data, 
            authentication=self.get_credentials()
        )

    def test_post_list(self):
        # Check how many are there first.
        self.assertEqual(UserAccessToken.objects.count(), 0)
        self.assertHttpCreated(self.post())
        # Verify a new one has been added.
        self.assertEqual(UserAccessToken.objects.count(), 1)

    def test_put_detail_unauthenticated(self):
        _tempEntry = self.post()
        _detail_url = self.detail_url.format(_tempEntry.json()[self.resource_pk])
        self.assertHttpMethodNotAllowed(self.api_client.put(_detail_url, format='json', data={}))

    def test_delete_detail(self):
        _tempEntry = self.post()
        _detail_url = self.detail_url.format(_tempEntry.json()[self.resource_pk])
        self.assertHttpAccepted(self.api_client.delete(_detail_url, format='json', authentication=self.get_credentials()))

    def test_get_list_json(self):
        resp = self.api_client.get(self.resource_list_endpoint, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)