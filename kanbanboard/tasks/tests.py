from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin, TestApiClient

#Import the auth models we need
from django.contrib.auth.models import User, Permission
#Model to be tested
from tasks.models import Task, Timelog
import datetime
import json
import yaml

# Setup our tests here.

class TaskResourceTest( ResourceTestCaseMixin, TestCase):
  fixtures = ['test_tasks.json']
  def setUp( self ):
    #Create a dummy task for the rest of the test cases.
    super(TaskResourceTest, self).setUp()
    #Fetch the test resource we made.
    self.task_one = Task.objects.get(name="Refactor the code.")
    #Save the detail url.
    self.detail_url = '/api/v1/task/{0}/'.format( self.task_one.pk )
    #We are saving this post data so that we can reuse it.
    self.post_data = {
      "name": "Refactor the code pt2.",
      "estimate": 3.00,
      "description":"Remove old controllers in the timelog module.",
      "is_archived": False,
      "total_time": 0.50,
    }
    self.maxDiff =None
    #Create an authorized user.
    authorized_user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='1234')
    #Give the task permission to the authorized user.
    task_change_perm = Permission.objects.get(name='Can change task')
    authorized_user.user_permissions.add( task_change_perm )
    self.authorized_user = authorized_user
    #Create an unauthorized user.
    unauthorized_user = User.objects.create_user(username='testuseru', email='testuseru@gmail.com', password='1234')
    self.unauthorized_user = unauthorized_user
    #Create API Client
    self.api_client = TestApiClient()
  #Check if we can get a JSON response when querying the list of objects.
  def get_credentials_auth( self ):
    res = self.api_client.client.login(username='testuser',password='1234')
    return res
  def get_credentials_unauth( self ):
    res = self.api_client.client.login(username='testuseru',password='1234')
    return res
  def test_get_list_unauthenticated( self ):
    #No authentication
    resp = self.api_client.get('/api/v1/task/', format='json')
    self.assertHttpUnauthorized(resp)

  def test_get_list_unauthorized( self ):
    #Login as the unauthorized user.
    resp = self.api_client.get('/api/v1/task/', format='json',authentication= self.get_credentials_unauth() )
    self.assertValidJSONResponse(resp)
    resourceData = yaml.safe_load( resp.content ) 
    resourceList = resourceData['objects']
    self.assertEqual( len( resourceList ), 0 )

  def test_get_list_json( self ):
    #Login as the authorized user.

    resp = self.api_client.get('/api/v1/task/', format='json',authentication= self.get_credentials_auth() )
    self.assertValidJSONResponse(resp)
    #Check that we have 1 task in the resource list.
    resourceData = yaml.safe_load( resp.content ) 
    resourceList = resourceData['objects']
    self.assertEqual( len( resourceList ), 1 )
    #Let's check the whole object.
    
    fixtureData = {
      "id":  self.task_one.pk ,
      "name": "Refactor the code.",
      "estimate": "2.00",
      "description":"Remove old controllers in the task module.",
      "is_archived": False,
      "total_time": "1.00",
      "created_at": "2016-08-08T08:32:05.641000",
      "modified_at":"2016-08-17T04:20:40.424000",
      "resource_uri": "/api/v1/task/{0}/".format(self.task_one.pk ) 
    }
    self.assertEqual( resourceList[0], fixtureData )
  #Check if we can get a JSON response when querying the list of objects.
    
  def test_get_detail_unauthenticated( self ):
    #No authentication
    resp = self.api_client.get(self.detail_url, format='json')
    self.assertHttpUnauthorized(resp)
  def test_get_detail_unauthorized( self ):
    #Login as the unauthorized user.
    resp = self.api_client.get(self.detail_url, format='json',authentication= self.get_credentials_unauth() )
    self.assertHttpUnauthorized(resp)
  def test_get_detail_json( self ):
    #Login as the authorized user.

    resp = self.api_client.get(self.detail_url, format='json',authentication= self.get_credentials_auth() )
    self.assertValidJSONResponse(resp)
    #Check that we have 1 task in the resource list.
    resourceData = yaml.safe_load( resp.content ) 
    #resourceList = resourceData['objects']
    #self.assertEqual( len( resourceList ), 1 )
    #Let's check the whole object.
    
    fixtureData = {
      "id":  self.task_one.pk ,
      "name": "Refactor the code.",
      "estimate": "2.00",
      "description":"Remove old controllers in the task module.",
      "is_archived": False,
      "total_time": "1.00",
      "created_at": "2016-08-08T08:32:05.641000",
      "modified_at":"2016-08-17T04:20:40.424000",
      "resource_uri": "/api/v1/task/{0}/".format(self.task_one.pk ) 
    }
    self.assertEqual( resourceData, fixtureData )
  #Check if we can get a JSON response when querying the list of objects.


