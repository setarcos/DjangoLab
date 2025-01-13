from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Survey

def index(request):
    survey = Survey.objects.all()
    return render(request, 'linux/index.html', {'survey': survey})
