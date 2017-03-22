from __future__ import unicode_literals
from django.db import models


# Create your models here.
class CommonInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Books(CommonInfo):
    author = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class UserDetail(CommonInfo):
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    books = models.ManyToManyField(Books)
