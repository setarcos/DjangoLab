from django.db import models
import datetime

class MeetingRoom(models.Model):
    room_no = models.CharField(max_length=15, verbose_name="房间号")
    info = models.CharField(max_length=200, blank=True, verbose_name="描述")

    class Meta:
        verbose_name="会议室"
        verbose_name_plural="会议室"

    def get_agenda(self):
        return self.agenda.all()

    # to check if the agenda is without conflict
    def isOK(self, day, start, end):
        return True


class RoomAgenda(models.Model):
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='agenda')
    title = models.CharField(max_length=200)
    userid = models.CharField(max_length=12)
    username = models.CharField(max_length=40)
    repeat = models.IntegerField(default=0)
    date = models.DateField(default='2018-01-01')
    week = models.IntegerField(default=-1)
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='00:00')

    def collide_time(self, other):
        if ((self.start_time < other.end_time) and (self.start_time > other.start_time)):
            return True
        if ((self.end_time > other.start_time) and (self.end_time < other.end_time)):
            return True
        return False

    def collide(self):
        today = datetime.date.today()
        all_agenda = RoomAgenda.objects.filter(room=self.room,date__gte=today)
        if self.repeat == 1:
            for a in all_agenda.filter(week=self.week,repeat=1):
                if self.collide_time(a):
                    return True
            for a in all_agenda.filter(date__lte=self.date,week=self.week,repeat=0):
                if self.collide_time(a):
                    return True
        else:
            for a in all_agenda.filter(date=self.date,repeat=0):
                if self.collide_time(a):
                    return True
            for a in all_agenda.filter(date__gte=self.date,week=self.week,repeat=1):
                if self.collide_time(a):
                    return True
        return False
