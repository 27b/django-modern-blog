from distutils.command.upload import upload
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=512)
    image = models.ImageField(upload_to='images/profile/')

    def __str__(self) -> str:
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.title


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

    def __str__(self) -> str:
        return self.title


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
