from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#class UserProfile(models.Model):
  #user = models.OneToOneField(User)

  #def __str__(self):
    #return "%s's profile" % self.user

class Circle(models.Model):
  users = models.ManyToManyField(User, related_name='circle_users')
  title = models.CharField(max_length=63)
  teacher = models.ForeignKey(User, related_name='circle_teacher')

class Genre(models.Model):
  name = models.CharField(max_length=63)
  image = models.URLField()

class Song(models.Model):
  time = models.TimeField(auto_now_add=True)
  user = models.ForeignKey(User, related_name='song_user')
  title = models.CharField(max_length=255)
  description = models.TextField()
  starred = models.ManyToManyField(User, related_name='song_starred')
  circle = models.ForeignKey(Circle)
  genre = models.ForeignKey(Genre)

class Comment(models.Model):
  song = models.ForeignKey(Song)

