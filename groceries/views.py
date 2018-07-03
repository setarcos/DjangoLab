from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Items, History
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone

@login_required
def index(request):
    item_list = Items.objects.all()[:5]
    return render(request, 'groceries/index.html', {'item_list': item_list})

from .forms import LendForm

def lenditem(request, lend_id):
    item = get_object_or_404(Items, pk=lend_id)
    if request.method == 'POST':
        form = LendForm(request.POST)
        if form.is_valid():
            if item.status == 0:
                item.status = 1
                hist = History(item = item)
                hist.user = request.POST.get('username', '')
                hist.tel = request.POST.get('telephone', '')
                hist.note = request.POST.get('note', '')
                hist.date = timezone.now()
                hist.save()
                item.save()
            return HttpResponseRedirect('/')
    else:
        if item.status == 1: # return the item
            item.status = 0
            item.save()
            hist = History.objects.filter(item=item).order_by('-date')
            if hist.count() >= 1:
                h = hist.first()
                h.back = timezone.now()
                h.save()
            return HttpResponseRedirect('/')
        form = LendForm();
    return render(request, 'groceries/lend.html', {'form': form})

def itemhist(request, lend_id):
    item = get_object_or_404(Items, pk=lend_id)
    hist = History.objects.filter(item=item).order_by('-date')
    return render(request, 'groceries/hist.html', {'hist': hist})
