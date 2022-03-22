from django.contrib import admin
from django import forms
from .models import Course, CourseGroup, LabRoom, SchoolYear, CourseSchedule

class CourseAdminForm(forms.ModelForm):
    term = forms.ChoiceField(
            label='开课学期',
            choices=((0, "春季"), (1, "秋季"), (2, "暑期")),
            )

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('name', 'ename', 'tea_id', 'tea_name','mailbox')
    list_filter = ['name']
    search_fields = ['name']

class CourseGroupAdmin(admin.ModelAdmin):
    list_display = ('course', 'week', 'room', 'tea_name', 'year', 'limit')

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(CourseSchedule)
admin.site.register(LabRoom)
admin.site.register(SchoolYear)
