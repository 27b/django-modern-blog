from django.contrib import admin
from . import models


admin.site.register(models.Profile)
admin.site.register(models.Category)
admin.site.register(models.Post)
admin.site.register(models.Contact)
admin.site.register(models.Subscriber)
