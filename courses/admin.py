from django.contrib import admin
from .models import Course, CourseGroup, LabRoom, SchoolYear, CourseSchedule

class CourseAdmin(admin.ModelAdmin):
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
