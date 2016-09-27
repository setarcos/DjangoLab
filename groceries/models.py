from __future__ import unicode_literals

from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class Items(models.Model):
    name = models.CharField(max_length=200)
    serial = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
    position = models.CharField(max_length=20)
    status = models.ForeignKey(Status)
    note = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class History(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    date = models.DateTimeField('Borrow/Return Date')
    tel = models.CharField(max_length=20)
