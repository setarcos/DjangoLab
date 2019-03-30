from django.contrib import admin
from .models import MeetingRoom

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'info')

admin.site.register(MeetingRoom, RoomAdmin)
