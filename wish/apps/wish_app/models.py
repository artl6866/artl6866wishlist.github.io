from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime
from ..app_one.models import *
from . models import *



class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['titlelength'] = "Please enter a product"

        return errors




class Item(models.Model):
    title = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, related_name = 'user_create', on_delete = 'models.CASCADE')
    user_wish = models.ManyToManyField(User, related_name='user_title')
    objects = ItemManager()


