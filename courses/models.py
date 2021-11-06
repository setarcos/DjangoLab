from django.db import models
from ckeditor.fields import RichTextField

class Course(models.Model):
    class Meta:
        verbose_name="课程"
        verbose_name_plural="课程"
    name = models.CharField(max_length=100, verbose_name="课程名")
    ename = models.CharField(max_length=200, verbose_name="课程英文名")
    ccode = models.CharField(max_length=20, verbose_name="课程号,学分,学时")
    term = models.IntegerField(default=0, verbose_name="开课学期")
    tea_id = models.CharField(max_length=10, verbose_name="负责人ID") # 负责人 ID
    tea_name = models.CharField(max_length=50, verbose_name="授课教师") # 可以输入多个教师名
    intro = RichTextField(verbose_name="课程大纲")
    mailbox=models.CharField(max_length=200, verbose_name="联系邮箱")
    def __str__(self):
        return self.name

class CourseGroup(models.Model):
    class Meta:
        verbose_name="课程分组"
        verbose_name_plural="课程分组"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    week = models.CharField(max_length=50, verbose_name="上课时间")
    room = models.CharField(max_length=10, verbose_name="上课地点")
    tea_name = models.CharField(max_length=10, verbose_name="授课教师")
    year = models.IntegerField(default=2020, verbose_name="学年") # 2020 代表 20-21 学年
    limit = models.IntegerField(default=15, verbose_name="人数限制")

class StudentGroup(models.Model):
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    stu_name = models.CharField(max_length=10, verbose_name="姓名")
    seat = models.IntegerField(default=0, verbose_name="座位")

class StudentHist(models.Model):
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    datetime = models.DateTimeField(default='2018-01-01', verbose_name="日期")
    room = models.CharField(max_length=10, verbose_name="上课地点")
    seat = models.IntegerField(default=0, verbose_name="座位")
    note = models.CharField(max_length=50, verbose_name="自记录")
    tea_note =models.CharField(max_length=50, verbose_name="教师记录")
    confirm = models.IntegerField(default=0, verbose_name="确认")
