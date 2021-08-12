from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Course

def index(request):
    course = Course.objects.all()
    return render(request, 'courses/index.html', {'course_list': course})
