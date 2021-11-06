from django.contrib import admin
from .models import Course, CourseGroup

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ename', 'tea_id', 'tea_name', 'intro', 'mailbox')
    list_filter = ['name']
    search_fields = ['name']

class CourseGroupAdmin(admin.ModelAdmin):
    list_display = ('course', 'week', 'room', 'tea_name', 'year', 'limit')

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
