# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(unique=True, max_length=32)
    nick = models.CharField(max_length=32)
    is_superuser = models.BooleanField(default=False, help_text=u'Super user got more power')

    def __unicode__(self):
        return self.name


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        user.save()
        user_profile = UserProfile(user=user, name=user.username, is_superuser=user.is_superuser)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Symbol(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField(blank=True, null=True)
    refresh =  models.BooleanField(default=True)
    creater = models.ForeignKey(UserProfile)
    create_at = models.DateTimeField(auto_now_add=True)
    enabled =  models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name)

    def toJSON(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

class Platform(models.Model):
    symbol = models.ForeignKey(Symbol)
    name = models.TextField(blank=True, null=True)
    home = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    xpath = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    refresh =  models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    creater = models.ForeignKey(UserProfile)
    create_at = models.DateTimeField(auto_now_add=True)
    enabled =  models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.symbol)

    def toJSON(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
