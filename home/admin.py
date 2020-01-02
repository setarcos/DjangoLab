from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'perm')

admin.site.register(Teacher, TeacherAdmin)
