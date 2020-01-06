from django.db import models

MEETING_ADMIN = 1  # 会议室确认权限

class Teacher(models.Model):

    class Meta:
        verbose_name="教师"
        verbose_name_plural="教师"

    name = models.CharField(max_length=200, verbose_name="姓名")
    uid = models.CharField(max_length=10, verbose_name="工作证号")
    perm = models.IntegerField(default=0, verbose_name="权限") # web permissions

    def is_meeting_admin(self):
        return self.perm & MEETING_ADMIN

    @staticmethod
    def is_meeting_admin(p):
        if p < 0:
            return False
        return p & MEETING_ADMIN
