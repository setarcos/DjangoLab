from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

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

class LabRoom(models.Model):
    class Meta:
        verbose_name="实验室"
        verbose_name_plural="实验室"
    name = models.CharField(max_length=10, verbose_name="房间号")
    cname = models.CharField(max_length=30, verbose_name="实验室名称")
    manager = models.CharField(max_length=10, verbose_name="负责人")
    def __str__(self):
        return self.name

class SchoolYear(models.Model):
    class Meta:
        verbose_name="学年"
        verbose_name_plural="学年"
    name = models.CharField(max_length=10, verbose_name="学期")
    start = models.DateField(default='2022-01-01', verbose_name="起始时间")
    end = models.DateField(default='2022-01-01', verbose_name="结束时间")
    def __str__(self):
        return self.name

    def get_wcount(self):
        now = timezone.now().date();
        return int((now - self.start).days / 7 + 1)

    @staticmethod
    def get_week():
        sy = SchoolYear.objects.all().order_by('-start');
        if sy.count() == 0:
            return -1
        return sy.first().get_wcount();

    @staticmethod
    def get_current_year():
        sy = SchoolYear.objects.all().order_by('-start');
        return sy.first()

    def get_status(self):
        now = timezone.now().date();
        if (now < self.start) or (now > self.end):
            return "假期"
        return self.name + f"学期，第 {self.get_wcount()} 周"

class CourseSchedule(models.Model):
    class Meta:
        verbose_name="课程安排"
        verbose_name_plural="课程安排"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    week = models.IntegerField(default=0, verbose_name="周")
    name = models.CharField(max_length=20, verbose_name="实验内容")
    require = models.CharField(max_length=50, verbose_name="实验要求", default="")
    def __str__(self):
        return self.name

class CourseGroup(models.Model):
    class Meta:
        verbose_name="课程分组"
        verbose_name_plural="课程分组"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    # 两位数，第一位代表星期，第二位代表上午下午和晚上，例如 72 代表周日晚上，0 代表特殊时间安排
    week = models.IntegerField(default=0, verbose_name="上课时间")
    room = models.ForeignKey(LabRoom, on_delete=models.CASCADE, verbose_name="上课地点")
    tea_name = models.CharField(max_length=10, verbose_name="授课教师")
    year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, verbose_name="学年")
    limit = models.IntegerField(default=15, verbose_name="人数限制")

class StudentGroup(models.Model):
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    stu_name = models.CharField(max_length=10, verbose_name="姓名")
    seat = models.IntegerField(default=0, verbose_name="座位")

class StudentHist(models.Model):
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    stu_name = models.CharField(max_length=10, verbose_name="姓名")
    group = models.ForeignKey(CourseGroup, on_delete=models.SET_NULL, verbose_name="课程名称", null=True)
    room = models.ForeignKey(LabRoom, on_delete=models.CASCADE, verbose_name="上课地点")
    seat = models.IntegerField(default=0, verbose_name="座位")
    lab_name = models.CharField(max_length=20, verbose_name="实验内容")
    note = models.CharField(max_length=50, verbose_name="自记录")
    tea_note =models.CharField(default="", max_length=50, verbose_name="教师记录")
    tea_name = models.CharField(max_length=10, verbose_name="教师姓名")
    fin_time = models.DateTimeField(default='2018-01-01 00:00:00', verbose_name="日期")  # confirm 时间
    confirm = models.IntegerField(default=0, verbose_name="确认")

class StudentLog(models.Model): # StudentEva might be a better name, since I use a lot eva to distinguish it from StudentHist
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    tea_name = models.CharField(max_length=10, verbose_name="教师")
    note = models.CharField(max_length=100, verbose_name="记录内容")
    note_time = models.DateTimeField(verbose_name="时间")
