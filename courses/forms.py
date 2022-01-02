from django import forms
from .models import LabRoom

class StuLabForm(forms.Form):
    stu_id = forms.CharField(
        label='学号',
        widget=forms.TextInput(attrs={'readonly':True}),
        )
    stu_name = forms.CharField(
        label='姓名',
        widget=forms.TextInput(attrs={'readonly':True}),
        )
    room = forms.ModelChoiceField(
        queryset=LabRoom.objects.all(),
        label='房间号',
        )
    seat = forms.IntegerField(
        max_value = 100,
        min_value = 1,
        )
    lab_name = forms.CharField(
        label='实验名称',
        )
    switch = forms.BooleanField(
        label='设备关机，烙铁断电',
        )
    table = forms.BooleanField(
        label='整理桌面',
        )
    note = forms.CharField(
        required=False,
        label='设备问题',
        )

    def clean(self):
        super().clean()
        if (not self.is_valid()):
            return
        s = self.cleaned_data.get('switch')
        e = self.cleaned_data.get('table')
        if (not s) or (not e):
            raise forms.ValidationError("必须先整理桌面和给设备关机")
