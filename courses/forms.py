from django import forms
from .models import LabRoom, CourseGroup, Course, CourseSchedule, StudentLog, CourseFiles
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget

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
        label='座位号',
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

class GroupForm(BSModalModelForm):
    nweek = forms.ChoiceField(
            label='星期',
            choices=((0, "不指定"), (1, "周一"), (2, "周二"), (3, "周三"), (4, "周四"),
                (5, "周五"), (6, "周六"), (7, "周日")),
            )
    npart = forms.ChoiceField(
            label='时间',
            choices=((0, "上午"), (1, "下午"), (2, "晚上"), (3, "后段下午"), (4, "后段晚上")),
            )
    modal_title = "增加时段"

    class Meta:
        model = CourseGroup
        fields = ['room', 'tea_name', 'limit']

class ScheduleForm(BSModalModelForm):
    require = forms.CharField(
            required = False,
            label='具体要求',
            )
    modal_title = "增加实验内容"

    class Meta:
        model = CourseSchedule
        fields = ['week', 'name', 'require']

class StudentEvaForm(BSModalModelForm):
    modal_title = "增加学生评价"
    stu_name = forms.CharField(
        label='姓名',
        widget=forms.TextInput(attrs={'readonly':True}),
        )

    forget = forms.BooleanField(
            label='学生未填写记录离开',
            required = False,
            )
    note = forms.CharField(
            label='记录内容',
            required = False,
            )
    class Meta:
        model = StudentLog
        fields = ['note', 'stu_name']

    def clean(self):
        cleaned_data = super(StudentEvaForm, self).clean()
        forget = cleaned_data.get('forget')
        note = cleaned_data.get('note')
        if (forget == False) and (note == ''):
            raise forms.ValidationError("必须填写内容")
        return cleaned_data

class EvaDayForm(forms.Form):
    edate = forms.DateField(
        label='实验时间',
        )
    nweek = forms.IntegerField(
        label='上课周次',
        )

class LabRoomQueryForm(forms.Form):
    sdate = forms.DateField(
        label='开始时间',
        )
    edate = forms.DateField(
        label='结束时间',
        )

class CourseForm(forms.ModelForm):
    term = forms.ChoiceField(
            label='开课学期',
            choices=((0, "春季"), (1, "秋季"), (2, "暑期")),
            )
    class Meta:
        model = Course
        exclude = ['ccode','tea_id']

class SeatForm(forms.Form):
    seat2 = forms.IntegerField(
        label = '新座位号',
        )

class UploadForm(forms.Form):
    finfo = forms.CharField(
        label = '文件描述'
        )
    file = forms.FileField(
        label = '文件'
        )
    course = None

    def clean(self):
        cleaned_data = super().clean()
        up_file = cleaned_data.get('file')
        files = CourseFiles.objects.filter(course=self.course, fname=up_file.name)
        if (files.count() > 0):
            raise forms.ValidationError("文件已经在服务器存在")
        return cleaned_data;
