from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Items
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    item_list = Items.objects.all()[:5]
    return render(request, 'groceries/index.html', {'item_list': item_list})

from .forms import LendForm

def lenditem(request):
    if request.method == 'POST':
        form = LendForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = LendForm();
    return render(request, 'groceries/lend.html', {'form': form})
