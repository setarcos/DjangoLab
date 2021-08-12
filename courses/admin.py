from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ename', 'tea_id', 'tea_name', 'intro', 'mailbox')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Course, CourseAdmin)
