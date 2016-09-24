from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
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
    self.detail_url = '/api/v1/task/{0}'.format( self.task_one.pk )
    #We are saving this post data so that we can reuse it.
    self.post_data = {
      "name": "Refactor the code pt2.",
      "estimate": 3.00,
      "description":"Remove old controllers in the timelog module.",
      "is_archived": False,
      "total_time": 0.50,
    }
    self.maxDiff =None
  #Useful functions
  def test_get_list_json( self ):
    resp = self.api_client.get('/api/v1/task/', format='json')
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
    


