from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    title = models.CharField(max_length=32, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    content = models.TextField()
    tags = ArrayField(models.CharField(max_length=32, blank=True))
    image = models.ImageField(upload_to='images/')
    last_modified = models.DateField(auto_now=True)
    datetime = models.DateTimeField(auto_now_add=True)
