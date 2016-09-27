# tasks/api.py
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tasks.models import Task,Timelog
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication

###Custom Authentication Class
# Anyone who is signed in can view the api.
class DjangoAuth(Authentication):
  def is_authenticated( self, request, **kwargs ):
    if request.user.username:
      return True
    return False
  def get_identifier( self, request ):
    return request.user.username
###Resources
class TaskResource(ModelResource):
  class Meta:
    #Define the queryset here.
    queryset = Task.objects.filter(is_archived=False) #We leave out the archived tasks.
    resource_name = 'task' #The name of your api resource.
    filtering = {
      'name': ALL, #Allow filtering by name
      'id': ALL, #Allow filtering by id
      'modified_at': ALL, #Allow filtering by last modified date.
    }
    authentication = DjangoAuth() #Allow users who are signed in to access the api.
    authorization = DjangoAuthorization() #Allow users who have the Django Permission for the Task model to make changes via the API.
class TimelogResource(ModelResource):
  task = fields.ToOneField( TaskResource,'task', full=True) #Define task as a foreign key resource and return the full details of the task object.
  class Meta:
    #Define the queryset here.
    queryset = Timelog.objects.all() #We leave out the archived tasks.
    resource_name = 'timelog' #The name of your api resource.
    filtering = {
      'task': ALL_WITH_RELATIONS, #Allow filtering by task and its properties.
    }
    authentication = DjangoAuth() #Allow users who are signed in to access the api.
    authorization = DjangoAuthorization() #Allow users who have the Django Permission for the Task model to make changes via the API.
