from django.shortcuts import render
from .models import Items
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    item_list = Items.objects.all()[:5]
    return render(request, 'groceries/index.html', {'item_list': item_list})
