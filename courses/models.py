from django.db import models
from ckeditor.fields import RichTextField

class Course(models.Model):
    class Meta:
        verbose_name="课程"
        verbose_name_plural="课程"
    name = models.CharField(max_length=100)
    ename = models.CharField(max_length=200)
    ccode = models.CharField(max_length=20) # 课程号,学分,学时 三个内容放在一个字段
    term = models.IntegerField(default=0)
    tea_id = models.CharField(max_length=10) # 负责人 ID
    tea_name = models.CharField(max_length=50) # 可以输入多个教师名
    intro = RichTextField()
    mailbox=models.CharField(max_length=200)
