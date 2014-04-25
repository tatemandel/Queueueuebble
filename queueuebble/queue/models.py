from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.ForeignKey(User)
  visited = models.ManyToManyField('Queue', related_name="visited")
  favorites = models.ManyToManyField('Queue', related_name="favorites")

  def __unicode__(self):
    return self.user.username

  class Meta:
    ordering = ('user',)

class Queue(models.Model):
  name = models.CharField(max_length=50)
  size = models.IntegerField(default=0)
  creator = models.ForeignKey(UserProfile, related_name="creator")
  owner = models.ManyToManyField(UserProfile)
  closed = models.BooleanField(default=False)
  
  def __unicode__(self):
    return self.name

  def contains(self, userProf):
    nodes = list(self.node_set.all())
    nodeUsers = map((lambda n: n.user), nodes)
    return userProf in nodeUsers

  class Meta:
    ordering = ('name',)

class Node(models.Model):
  queue = models.ForeignKey(Queue)
  user = models.ForeignKey(UserProfile)
  position = models.IntegerField(default=0)
  status = models.IntegerField(default=0)

  def __unicode__(self):
    return self.user.user.username

  def getStatus(self):
    if self.status == 0: return "Not started"
    elif self.status == 1: return "In progress"
    else: return "Completed"

  def changeStatus(self, toStatus):
    if toStatus == "Not started":
      self.status = 0
    elif toStatus == "In progress":
      self.status = 1
    else: self.status = 2

  class Meta:
    ordering = ('queue', 'position', 'user')
