from django.contrib import admin
from .models import Survey

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('course', 'info', 'flag', 'sweek', 'eweek')

admin.site.register(Survey, SurveyAdmin)
