from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Course, CourseGroup

def index(request):
    course_all = Course.objects.all()
    return render(request, 'courses/index.html', {'course_list': course_all})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    group = CourseGroup.objects.filter(course=course)
    return render(request, 'courses/detail.html', {'course': course, 'group': group})
