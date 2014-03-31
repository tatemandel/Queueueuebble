from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.ForeignKey(User)

  def __unicode__(self):
    return self.user.username

  class Meta:
    ordering = ('user',)

class Queue(models.Model):
  name = models.CharField(max_length=50)
  size = models.IntegerField(default=0)
  owner = models.ManyToManyField(UserProfile)
  
  def __unicode__(self):
    return self.name
 
  class Meta:
    ordering = ('name',)

class Node(models.Model):
  queue = models.ForeignKey(Queue)
  user = models.ForeignKey(UserProfile)
  position = models.IntegerField(default=0)

  def __unicode__(self):
    return self.user.user.username

  class Meta:
    ordering = ('queue', 'user')
