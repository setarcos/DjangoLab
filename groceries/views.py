from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Items, History
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from home.models import Teacher

def getTea(request):
    try:
        tea = Teacher.objects.get(uid = request.session['schoolid'])
    except Teacher.DoesNotExist:
        raise Http404("没有数据")
    except KeyError:
        raise Http404("非标准用户或未登录")
    return tea

def index(request):
    tea = getTea(request)
    paginator = Paginator(Items.objects.all(), 25)
    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'groceries/index.html', {'item_list': items})

from .forms import LendForm, NewItem

def lendItem(request, lend_id):
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
            return HttpResponseRedirect(reverse('groceries:index'))
    else:
        if item.status == 1: # return the item
            item.status = 0
            item.save()
            hist = History.objects.filter(item=item).order_by('-date')
            if hist.count() >= 1:
                h = hist.first()
                h.back = timezone.now()
                h.save()
            return HttpResponseRedirect(reverse('groceries:index'))
        form = LendForm();
    return render(request, 'groceries/lend.html', {'form': form, 'f':'lend'})

def newItem(request):
    tea = getTea(request)
    if request.method == 'POST':
        form = NewItem(request.POST)
        if form.is_valid():
            item = Items(owner = tea)
            item.name = request.POST.get('itemname','')
            item.serial = request.POST.get('serial','')
            item.value = request.POST.get('value','')
            item.position = request.POST.get('room','')
            item.note = request.POST.get('note','')
            item.save()
            return HttpResponseRedirect('/items/')
    else:
        form = NewItem();
    return render(request, 'groceries/lend.html', {'form': form, 'f':'new'})

def editItem(request, lend_id):
    item = get_object_or_404(Items, pk=lend_id)
    if request.method == 'POST':
        form = NewItem(request.POST)
        if form.is_valid():
            item.name = request.POST.get('itemname','')
            item.serial = request.POST.get('serial','')
            item.value = request.POST.get('value','')
            item.position = request.POST.get('room','')
            item.note = request.POST.get('note','')
            item.save()
            return HttpResponseRedirect('/items/')
    else:
        form = NewItem(
            initial={'itemname': item.name,
                'serial': item.serial,
                'value': item.value,
                'room': item.position,
                'note': item.note});
    return render(request, 'groceries/lend.html', {'form': form, 'f':'new'})

def delItem(request, lend_id):
    item = get_object_or_404(Items, pk=lend_id)
    item.delete()
    return HttpResponseRedirect('/items/')

def itemHist(request, lend_id):
    item = get_object_or_404(Items, pk=lend_id)
    hist = History.objects.filter(item=item).order_by('-date')
    return render(request, 'groceries/hist.html', {'hist': hist})
