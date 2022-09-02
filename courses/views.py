from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, CourseGroup, StudentGroup, StudentHist
from .models import SchoolYear, CourseSchedule, StudentLog, LabRoom
from home.models import Teacher
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from filelock import FileLock
from os import remove
from django.utils import timezone
from datetime import timedelta

from .forms import StuLabForm, GroupForm, ScheduleForm, StudentEvaForm, LabRoomQueryForm, CourseForm, EvaDayForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

def index(request):
    course_all = Course.objects.all()
    return render(request, 'courses/index.html', {'course_list': course_all})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/detail.html', {'course': course})

def groups(request, course_id):
    if not 'schoolid' in request.session:
        raise Http404("登录才可以查看")
    course = get_object_or_404(Course, pk=course_id)
    year = SchoolYear.get_current_year() # only current year
    group = list(CourseGroup.objects.filter(course=course,year=year))
    for i in range(len(group)):
        m = StudentGroup.objects.filter(group=group[i].id,stu_id = request.session['schoolid'])
        if m.count() > 0:
            group[i].has_me=1
        else:
            group[i].has_me=0
    return render(request, 'courses/groups.html', {'course': course, 'group': group})

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
    lockfile = FileLock(f"/tmp/group.{group_id}")
    with lockfile:
        student = StudentGroup.objects.filter(group=group)
        m = StudentGroup(group = group)
        m.stu_id = request.session['schoolid']
        m.stu_name = request.session['realname']
        if (student.count() > 0):
            m.seat = student.order_by('-seat')[0].seat + 1
        else:
            m.seat = 1
        m.save()
    remove(f"/tmp/group.{group_id}")
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

def leaveGroup(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    m = StudentGroup.objects.filter(group=group,stu_id=request.session['schoolid'])
    if (m.count() > 0):
        m.delete()
    student = StudentGroup.objects.filter(group=group)
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

def logAdd(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    cur_id = request.session['schoolid']
    now = timezone.now() + timedelta(hours=-5) # 五小时以内
    old_his = StudentHist.objects.filter(stu_id=cur_id,fin_time__gte=now).order_by('-fin_time');
    if request.method == 'POST':
        form = StuLabForm(request.POST)
        if form.is_valid() and (form.cleaned_data['stu_id'] == cur_id):
            if (old_his.count() > 0) and (old_his.first().confirm == 1):
                return HttpResponseRedirect(reverse('home:index'))
            if (old_his.count() > 0):  # not confirmed entry can be overwrited (e.g. change seat no.)
                history = old_his.first() # update the last log
            else:
                history = StudentHist()
            history.stu_id = cur_id
            history.stu_name = form.cleaned_data['stu_name']
            history.room = form.cleaned_data['room']
            history.seat = form.cleaned_data['seat']
            history.lab_name = form.cleaned_data['lab_name']
            history.note = form.cleaned_data['note']
            history.fin_time = timezone.now()
            history.group = group
            history.save()
            return HttpResponseRedirect(reverse('home:index'))
    else:
        his_dfl = StudentHist()
        if (old_his.count() > 0):
            his_dfl = old_his.first()
        else:
            his_dfl.stu_id = cur_id;
            his_dfl.stu_name = request.session['realname']
            his_dfl.room = group.room
            student = StudentGroup.objects.filter(group=group,stu_id=cur_id)
            if (student.count() > 0):
                his_dfl.seat = student[0].seat
            else:
                his_dfl.seat = 0;
            week = SchoolYear.get_week()
            lab = CourseSchedule.objects.filter(course=group.course,week=week)
            if (lab.count() > 0):
                his_dfl.lab_name = lab[0].name
        initials = {}
        initials['stu_id'] = cur_id
        initials['stu_name'] = his_dfl.stu_name
        initials['room'] = his_dfl.room
        initials['seat'] = his_dfl.seat
        initials['lab_name'] = his_dfl.lab_name
        initials['note'] = his_dfl.note
        form = StuLabForm(initials)
    return render(request, 'courses/log_add.html', {'form': form})

def logConfirm(request, log_id):
    log = get_object_or_404(StudentHist, pk=log_id)
    if request.user.username != 'Teacher':
        raise Http404("只有教师具有此权限")
    log.tea_name = request.session['realname']
    log.fin_time = timezone.now()
    log.confirm = 1
    log.save()
    return HttpResponseRedirect(reverse('courses:logView', args=(log.group_id,)))

def updateSeat(request, log_id):
    log = get_object_or_404(StudentHist, pk=log_id)
    if request.user.username != 'Teacher':
        raise Http404("只有教师具有此权限")
    student = StudentGroup.objects.filter(group=log.group, stu_id=log.stu_id).first()
    if student:
        student.seat = log.seat
        student.save()
    return HttpResponseRedirect(reverse('courses:logView', args=(log.group_id,)))

def logView(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    if request.user.username != 'Teacher':
        raise Http404("只有教师具有此权限")
    students = list(StudentGroup.objects.filter(group=group).order_by('seat'))
    time_begin = timezone.now() + timedelta(hours=-5)
    logs = StudentHist.objects.filter(group=group,fin_time__gte=time_begin)
    all_logs = {}
    for log in logs:
        all_logs[log.stu_id] = log
    for i in range(len(students)):
        if students[i].stu_id in all_logs:
            students[i].complete = 1
            students[i].note = all_logs[students[i].stu_id].note
            students[i].confirmed = all_logs[students[i].stu_id].confirm
            students[i].log_id = all_logs[students[i].stu_id].id
            if students[i].seat != all_logs[students[i].stu_id].seat:
                students[i].new_seat = all_logs[students[i].stu_id].seat
            else:
                students[i].new_seat = 0
        else:
            students[i].complete = 0
    return render(request, 'courses/log_view.html', {'object_list':students, 'group':group})

class AddGroupView(BSModalCreateView):
    template_name = 'courses/form_temp.html'
    form_class = GroupForm

    def get_success_url(self):
        return reverse('courses:groups', kwargs={'course_id': self.kwargs['course_id']})

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['course_id'])
        if self.request.session['schoolid'] != course.tea_id:
            return HttpResponseRedirect(reverse('courses:groups', args=(course.id,)))
        form.instance.course_id = self.kwargs['course_id']
        form.instance.year_id = SchoolYear.get_current_year().id
        form.instance.week = int(form.cleaned_data['nweek']) * 10 + int(form.cleaned_data['npart'])
        return super().form_valid(form)

def delGroup(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    course = group.course
    if request.session['schoolid'] == course.tea_id:
        group.delete()
    return HttpResponseRedirect(reverse('courses:groups', args=(course.id,)))

class ScheduleListView(ListView):
    model = CourseSchedule
    template_name = 'courses/schedules.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseSchedule.objects.filter(course=self.course).order_by('week')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        context['course'] = course
        return context

class AddScheduleView(BSModalCreateView):
    template_name = 'courses/form_temp.html'
    form_class = ScheduleForm

    def get_success_url(self):
        return reverse('courses:schedules', kwargs={'course_id': self.kwargs['course_id']})

    def get_initial(self):
        s = CourseSchedule.objects.filter(course=self.kwargs['course_id']).order_by('-week')
        if (s.count() > 0):
            return {'week':s[0].week + 1,}
        else:
            return {'week':'1',}

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['course_id'])
        if self.request.session['schoolid'] != course.tea_id:
            return HttpResponseRedirect(reverse('courses:schedules', args=(course.id,)))
        form.instance.course_id = self.kwargs['course_id']
        return super().form_valid(form)

class UpdateScheduleView(BSModalUpdateView):
    template_name = 'courses/form_temp.html'
    form_class = ScheduleForm
    model = CourseSchedule

    def get_success_url(self):
        sched = CourseSchedule.objects.get(pk=self.kwargs['pk'])
        return reverse('courses:schedules', kwargs={'course_id': sched.course.id})

    def form_valid(self, form):
        sched = CourseSchedule.objects.get(pk=self.kwargs['pk'])
        if self.request.session['schoolid'] != sched.course.tea_id:
            return HttpResponseRedirect(reverse('courses:schedules', args=(sched.course.id,)))
        form.instance.course_id = sched.course.id
        return super().form_valid(form)

def delSchedule(request, sche_id):
    sche = get_object_or_404(CourseSchedule, pk=sche_id)
    course = sche.course
    if request.session['schoolid'] == course.tea_id:
        sche.delete()
    return HttpResponseRedirect(reverse('courses:schedules', args=(course.id,)))

class AddStudentEvaView(BSModalCreateView):
    template_name = 'courses/form_temp.html'
    form_class = StudentEvaForm

    def get_success_url(self):
        return reverse('courses:logView', kwargs={'group_id': self.kwargs['group_id']})

    def get_initial(self):
        stu = StudentGroup.objects.get(stu_id=self.kwargs['stu_id'],group=self.kwargs['group_id'])
        if (stu):
            return {'stu_name':stu.stu_name,}
        else:
            return {'stu_name':'42',}

    def form_valid(self, form):
        group = CourseGroup.objects.get(pk=self.kwargs['group_id'])
        if self.request.user.username != 'Teacher':
            return HttpResponseRedirect(reverse('home:index'))
        form.instance.group_id = self.kwargs['group_id']
        form.instance.stu_id = self.kwargs['stu_id']
        form.instance.tea_name = self.request.session['realname']
        form.instance.note_time = timezone.now()
        if form.cleaned_data['forget']==True:
            now = timezone.now() + timedelta(hours=-1) # 1小时以内
            old_his = StudentHist.objects.filter(stu_id=self.kwargs['stu_id'],fin_time__gte=now).order_by('-fin_time');
            if (old_his.count() == 0):  # 这里可能会有竞争条件，但暂时忽略
                hist = StudentHist()
                hist.stu_id = self.kwargs['stu_id']
                student = StudentGroup.objects.filter(group=group,stu_id=self.kwargs['stu_id'])
                if (student.count() > 0):
                    hist.seat = student[0].seat
                    hist.stu_name = student[0].stu_name
                else:
                    hist.seat = 0;
                    hist.stu_name = '未知'
                week = SchoolYear.get_week()
                lab = CourseSchedule.objects.filter(course=group.course,week=week)
                if (lab.count() > 0):
                    hist.lab_name = lab[0].name
                else:
                    hist.lab_name = '未知'
                hist.room = group.room
                hist.note = '学生忘记记录'
                hist.fin_time = timezone.now();
                hist.group = group
                hist.confirm = 1
                hist.save()
        return super().form_valid(form)

def evaView(request, group_id, stu_id):
    if request.user.username != 'Teacher':
        raise Http404("用户没有权限")
    m = StudentGroup.objects.filter(group_id=group_id,stu_id=stu_id)
    if m.count() == 0:
        raise Http404("没有这个学生");
    sl = StudentLog.objects.filter(group_id=group_id,stu_id=stu_id).order_by('note_time')
    return render(request, 'courses/eva_list.html', {'object_list': sl, 'student_name':m.first().stu_name})

def evaDayView(request, group_id):
    if not 'userperm' in request.session:
        raise Http404("用户没有登陆")
    if request.user.username != 'Teacher':
        raise Http404("用户没有权限")

    course = get_object_or_404(CourseGroup, pk=group_id);
    edate = timezone.now().date()
    nweek = course.year.get_wcount()
    if (nweek > 18):
        nweek = 18
    if request.method == 'POST':
        form = EvaDayForm(request.POST)
        if form.is_valid():
            edate = form.cleaned_data['edate']
            nweek = form.cleaned_data['nweek']
    if (nweek > 0): # ignore edate
        week = course.week / 10 - 1 # Weekday
        delta = nweek * 7 + week
        edate = course.year.start + timedelta(days=delta)
    initials = {}
    initials['edate'] = edate
    initials['nweek'] = nweek
    form = EvaDayForm(initials)
    history = list(StudentGroup.objects.filter(group=group_id).order_by('seat'))
    for i in range(len(history)):
        history[i].log = list(StudentLog.objects.filter(group=group_id,stu_id=history[i].stu_id,note_time__gte=edate,note_time__lte=edate + timedelta(days=1)))
    return render(request, 'courses/eva_day.html', {'form': form, 'hist': history})

def delEva(request, pk):
    log = get_object_or_404(StudentLog, pk=pk)
    if request.session['realname'] == log.tea_name:
        log.delete()
    return HttpResponseRedirect(reverse('courses:evaView', args=(log.group.id,log.stu_id,)))

class RoomListView(ListView):
    model = LabRoom
    template_name = 'courses/rooms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perm'] = Teacher.is_lab_admin(self.request)
        return context

def roomDetail(request, room_id):
    room = get_object_or_404(LabRoom, pk=room_id)
    if not 'userperm' in request.session:
        raise Http404("用户没有登陆")
    if not Teacher.is_lab_admin(request):
        raise Http404("用户没有权限")

    edate = timezone.now().date()
    sdate = edate + timedelta(days=-1)
    if request.method == 'POST':
        form = LabRoomQueryForm(request.POST)
        if form.is_valid():
            sdate = form.cleaned_data['sdate']
            edate = form.cleaned_data['edate']
    history = StudentHist.objects.filter(room=room, fin_time__gte=sdate, fin_time__lte=(edate + timedelta(days=1))).order_by('fin_time')
    number = history.count()
    initials = {}
    initials['sdate'] = sdate
    initials['edate'] = edate
    form = LabRoomQueryForm(initials)
    return render(request, 'courses/room_detail.html', {'form': form, 'hist': history, 'number': number})

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_update.html'
    form_class = CourseForm

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'course_id': self.kwargs['pk']})

    def form_valid(self, form):
        if self.request.session['schoolid'] != form.instance.tea_id:
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
