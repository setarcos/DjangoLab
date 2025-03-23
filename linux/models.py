from django.db import models
from courses.models import Course
from django.utils import timezone

class Survey(models.Model):
    class Meta:
        verbose_name="调查问题"
        verbose_name_plural="调查问题"
    SurveyType = [
        (1, "上传公钥"),
        (2, "创建 git 账号"),
        (3, "检查 VIM 作业"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    flag = models.IntegerField(default=0, verbose_name="类别", choices=SurveyType)
    sweek = models.IntegerField(default=1, verbose_name="开始周")
    eweek = models.IntegerField(default=2, verbose_name="结束周")

    def get_flag_display(self):
        return dict(self.SurveyType).get(self.flag, "Unknown")

class Answer(models.Model):
    class Meta:
        verbose_name="学生答案"
        verbose_name_plural="学生答案"
    flag = models.IntegerField(default=0, verbose_name="类别")
    stu_id = models.CharField(max_length=10, verbose_name="学号")
    answer = models.CharField(max_length=200, verbose_name="答案")
    atime = models.DateTimeField(default=timezone.now().date(), verbose_name="回答时间")
