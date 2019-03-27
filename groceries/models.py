from django.db import models
from home.models import Teacher

class Items(models.Model):
    name = models.CharField(max_length=200)
    serial = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
    position = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    note = models.CharField(max_length=200)
    owner = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    def __unicode__(self):
        return self.name

class History(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    date = models.DateTimeField('Borrow Date')
    tel = models.CharField(max_length=20)
    note = models.CharField(max_length=200)
    back = models.DateTimeField('Return Date', blank=True, null=True)
