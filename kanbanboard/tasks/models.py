from __future__ import unicode_literals

from django.db import models

# Create your models here.
#-------------------------------------------------------------------#
# Simple Task Model                                                 #
#-------------------------------------------------------------------#
class Task( models.Model ):
  name = models.CharField(max_length=100)
  estimate = models.DecimalField(max_digits=5,decimal_places=2,default=1.00)
  description = models.TextField()
  is_archived = models.BooleanField(default=False)
  total_time = models.DecimalField(max_digits=5,decimal_places=2)
#-------------------------------------------------------------------#
# Simple Timelog Model                                              #
#-------------------------------------------------------------------#
class Timelog( models.Model ):
  name = models.CharField(max_length=100)
  periodStart = models.DateTimeField() 
  periodEnd = models.DateTimeField() 
  task = models.ForeignKey( Task )
