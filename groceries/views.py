from django.shortcuts import render
from .models import Items

def index(request):
    item_list = Items.objects.all()[:5]
    return render(request, 'groceries/index.html', {'item_list': item_list})
