from django import forms
from django.utils import timezone
from .models import RoomAgenda, MeetingRoom

class AgendaForm(forms.Form):
    repeatable = forms.ChoiceField(
        required=True,
        label="日程类型",
        error_messages={'required': "日程类型必须选择"},
        choices=((1, "固定日期"), (2, "每周重复")),
        widget=forms.RadioSelect,
    )

    date = forms.DateField(
        required=False,
        label="日期",
        initial=timezone.now().date(),
#        widget=forms.SelectDateWidget,
    )

    week = forms.ChoiceField(
        required=False,
        label="星期",
        choices=((0, "周一"), (1, "周二"), (2, "周三"), (3, "周四"),
            (4, "周五"), (5, "周六"), (6, "周日")),
    )

    start = forms.TimeField(
        required=True,
        label="起始时间",
        widget=forms.TimeInput(attrs={'title':"时间格式：HH:MM"}),
    )

    end = forms.TimeField(
        required=True,
        label="结束时间",
        widget=forms.TimeInput(attrs={'title':"时间格式：HH:MM"}),
    )

    note = forms.CharField(
        required=True,
        label="事由",
        initial="",
    )

    def clean(self):
        super().clean()
        if (not self.is_valid()):
            return
        s = self.cleaned_data.get('start')
        e = self.cleaned_data.get('end')
        if (s >= e):
            raise forms.ValidationError("起始时间要早于结束时间")
        d = self.cleaned_data.get('date')
        if (d < timezone.now().date()):
            raise forms.ValidationError("日期不能在过去")
