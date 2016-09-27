from django.contrib import admin
from .models import Status, Items

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'position', 'status')

admin.site.register(Status)
admin.site.register(Items, ItemsAdmin)
