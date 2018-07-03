from django.contrib import admin
from .models import Items

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'position')

admin.site.register(Items, ItemsAdmin)
