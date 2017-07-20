# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Symbol(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return unicode(self.name)

class Market(models.Model):
    #symbol = models.CharField(max_length=16)
    symbol = models.ForeignKey(Symbol)
    platform = models.TextField(blank=True, null=True)
    home = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    enabled =  models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.symbol)

