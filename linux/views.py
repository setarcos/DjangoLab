from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Survey, Answer
from .forms import PubkeyForm
from courses.models import SchoolYear, CourseGroup, StudentGroup
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

def index(request):
    year = SchoolYear.get_current_year()
    cg = CourseGroup.objects.filter(year=year)
    survey = None
    if not 'schoolid' in request.session:
        raise Http404("用户没有登陆")
    for g in cg:
        sg = StudentGroup.objects.filter(group=g,stu_id=request.session['schoolid'])
        if sg.count() > 0:
            survey = Survey.objects.filter(course=g.course)
            if (survey.count() > 0):
                break
    return render(request, 'linux/index.html', {'survey': survey})

def in_course(request):
    if 'linux' in request.session:
        return True
    if not 'schoolid' in request.session:
        return False
    year = SchoolYear.get_current_year()
    cg = CourseGroup.objects.filter(year=year)
    for g in cg:
        sg = StudentGroup.objects.filter(group=g,stu_id=request.session['schoolid'])
        if sg.count() > 0:
            survey = Survey.objects.filter(course=g.course)
            if (survey.count() > 0):
                request.session['linux'] = True
                return True
    return false

def pubkey(request):
    if not in_course(request):
        raise Http404("用户没有权限")
    if request.method == 'POST':
        form = PubkeyForm(request.POST)
        if form.is_valid():
            ans = Answer.objects.filter(flag=1,stu_id=request.session['schoolid'])
            if ans.count() > 0:
                key = ans.first()
            else:
                key = Answer()
                key.flag = 1
                key.stu_id = request.session['schoolid']
            key.answer = form.cleaned_data['pubkey']
            key.atime = timezone.now()
            key.save()
            messages.success(request, "公钥保存成功")
            return HttpResponseRedirect(reverse('linux:index'))
    form = PubkeyForm()
    form.fields['stu_id'].initial = request.session['schoolid']
    return render(request, 'linux/pubkey.html', {'form': form})

