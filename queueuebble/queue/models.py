from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  def __unicode__(self):
    return self.user.username

class Queue(models.Model):
  name = models.CharField(max_length=50)
  owner = models.ManyToManyField(UserProfile)
  size = models.IntegerField(default=0)
  
  def __unicode__(self):
    return self.name

class Node(models.Model):
  queue = models.ForeignKey(Queue)
  user = models.ForeignKey(UserProfile)
  position = models.IntegerField(default=0)

  def __unicode__(self):
    return self.user.username
