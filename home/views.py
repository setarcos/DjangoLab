from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from courses.models import SchoolYear, CourseGroup, StudentGroup, StudentHist

import hashlib
import requests
import json
from datetime import timedelta

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('static/login.html')
    sy = SchoolYear.objects.all().order_by('-start');
    if sy.count() == 0:
        raise Http404("没有定义学期");
    year = sy.first() # current school season
    cg = CourseGroup.objects.filter(year=year) # all lab sessions
    course_list = []
    if request.user.username == 'Student':
        for g in cg:
            sg = StudentGroup.objects.filter(group=g,stu_id=request.session['schoolid'])
            if sg.count() > 0:
                now = timezone.now() + timedelta(hours=-5) # 五小时以内
                sh = StudentHist.objects.filter(group=g, stu_id=request.session['schoolid'],confirm=1,fin_time__gte=now)
                if (sh.count() > 0):
                    g.complete = 1  # 每天只能完成一个实验一次，其他时间也可以重复记录
                else:
                    g.complete = 0
                course_list.append(g)
    else:
        for g in cg:
            if g.tea_name == request.session['realname']:
                course_list.append(g);
    return render(request, 'home/index.html', {'schoolyear':year, 'courses':course_list})

def auth(request):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    KEY='7028D67CD5F82F92E0530100007F7A7D'
    ip=get_client_ip(request)
    token=request.GET.get('token', '')
    if (token == 'Student') or (token == 'Teacher'): # database should has those two
        u = User.objects.filter(username=token)
        if u.count() == 0:
            raise Http404('Invalid login')
        login(request, u.first())
        request.session['realname'] = request.GET.get('name', '贾鸣')
        request.session['schoolid'] = request.GET.get('id', '123456')
        return HttpResponseRedirect('/')

    para='appId=EELABWeb&remoteAddr='+ip+'&token='+token+KEY
    m=hashlib.md5()
    m.update(para.encode('utf-8'))
    url='https://iaaa.pku.edu.cn/iaaa/svc/token/validate.do'
    payload={'appId': 'EELABWeb', 'remoteAddr': ip, 'token': token, 'msgAbs': m.hexdigest()}
    r=requests.get(url, params=payload)
    data=json.loads(r.text)
    if data['errCode'] != '0':
        return HttpResponseRedirect('/')
    uid=data['userInfo']['identityId']
    utp=data['userInfo']['identityType']
    user=None
    if utp=='学生':
        u=User.objects.filter(username='Student')
        if u.count() > 0:
            user = u.first()
    if utp=='职工':
        u=User.objects.filter(username=uid)
        if u.count() == 0:
            u=User.objects.filter(username='Teacher')
        if u.count() > 0:
            user = u.first()
    if user:
        login(request, user)
        request.session['realname'] = data['userInfo']['name']
        request.session['schoolid'] = uid
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

