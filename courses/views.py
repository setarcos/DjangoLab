from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from .models import Course, CourseGroup, StudentGroup, StudentHist

def index(request):
    course_all = Course.objects.all()
    return render(request, 'courses/index.html', {'course_list': course_all})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    group = CourseGroup.objects.filter(course=course)
    for g in group.all():
        m = StudentGroup.objects.filter(group=g,stu_id = request.session['schoolid'])
        if m.count() > 0:
            request.session["has_me"]=g.id
    return render(request, 'courses/detail.html', {'course': course, 'group': group})

def groupDetail(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    student = StudentGroup.objects.filter(group=group).order_by('seat')
    return render(request, 'courses/group_detail.html', {'group': student})

def joinGroup(request, group_id):
    if request.user.username != 'Student':
        raise Http404("你必须是学生才可以选课")
    group = get_object_or_404(CourseGroup, pk=group_id)
    allgroup = CourseGroup.objects.filter(course=group.course)
    for g in allgroup.all():
        m = StudentGroup.objects.filter(group=g,stu_id = request.session['schoolid'])
        if (m.count() > 0):
            if (g == group):
                raise Http404("你已经在这个组里面了")
            else:
                raise Http404("你在这个课的其他组里")
    student = StudentGroup.objects.filter(group=group)
    m = StudentGroup(group = group)
    m.stu_id = request.session['schoolid']
    m.stu_name = request.session['realname']
    if (student.count() > 0):
        m.seat = student.order_by('-seat')[0].seat + 1
    else:
        m.seat = 1
    m.save()
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

def leaveGroup(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    m = StudentGroup.objects.filter(group=group,stu_id=request.session['schoolid'])
    if (m.count() > 0):
        m.delete()
    student = StudentGroup.objects.filter(group=group)
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

