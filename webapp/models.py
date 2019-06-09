from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Nationality(models.Model):
    name = models.CharField(max_length=20)


class Employee(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    nationality = models.ForeignKey(Nationality)


class Student(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)

class UserKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userkeys')
    secret_key = models.CharField(max_length = 255)
    class Meta:
        ordering = ['-id']

def __str__(self):
    return "{} secret key {}".format(self.user, self.secret_key)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ManyToManyField(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()


    def __str__(self):
        return self.headline

class Bookmark(models.Model):
	is_bookmarked = models.BooleanField(default=False)
	blog =models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookmarks')
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookmark_users')





