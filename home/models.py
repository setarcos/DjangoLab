from django.db import models

class Teacher(models.Model):
    uid = models.CharField(max_length=10)
    perm = models.IntegerField(default=0) # web permissions
