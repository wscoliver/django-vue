# tasks/api.py
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tasks.models import Task,Timelog
from tastypie.authorization import Authorization

class TaskResource(ModelResource):
  class Meta:
    #Define the queryset here.
    queryset = Task.objects.filter(is_archived=False) #We leave out the archived tasks.
    resource_name = 'task' #The name of your api resource.
    authorization = Authorization() #Very unsafe.For learning purposes only.
    filtering = {
      'name': ALL, #Allow filtering by name
      'id': ALL, #Allow filtering by id
      'modified_at': ALL, #Allow filtering by last modified date.
    }
class TimelogResource(ModelResource):
  task = fields.ToOneField( TaskResource,'task', full=True) #Define task as a foreign key resource and return the full details of the task object.
  class Meta:
    #Define the queryset here.
    queryset = Timelog.objects.all() #We leave out the archived tasks.
    resource_name = 'timelog' #The name of your api resource.
    authorization = Authorization() #Very unsafe.For learning purposes only.
    filtering = {
      'task': ALL_WITH_RELATIONS, #Allow filtering by task and its properties.
    }
