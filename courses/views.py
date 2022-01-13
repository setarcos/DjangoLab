from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, CourseGroup, StudentGroup, StudentHist, SchoolYear, CourseSchedule
from django.views.generic.list import ListView

from filelock import FileLock
from os import remove
from datetime import datetime, time

def index(request):
    course_all = Course.objects.all()
    return render(request, 'courses/index.html', {'course_list': course_all})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/detail.html', {'course': course})

def groups(request, course_id):
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
    lockfile = FileLock(f"group.{group_id}")
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
    remove(f"group.{group_id}")
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

def leaveGroup(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    m = StudentGroup.objects.filter(group=group,stu_id=request.session['schoolid'])
    if (m.count() > 0):
        m.delete()
    student = StudentGroup.objects.filter(group=group)
    return render(request, 'courses/group_detail.html', {'group': student.order_by('seat')})

from .forms import StuLabForm, GroupForm, ScheduleForm
from bootstrap_modal_forms.generic import BSModalCreateView

def logAdd(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    cur_id = request.session['schoolid']
    old_his = StudentHist.objects.filter(stu_id=cur_id,confirm=0).order_by('-fin_time');
    if request.method == 'POST':
        form = StuLabForm(request.POST)
        if form.is_valid() and (form.cleaned_data['stu_id'] == cur_id):
            if (old_his.count() > 0):
                history = old_his.first() # update the last log
            else:
                history = StudentHist()
            history.stu_id = cur_id
            history.stu_name = form.cleaned_data['stu_name']
            history.room = form.cleaned_data['room']
            history.seat = form.cleaned_data['seat']
            history.lab_name = form.cleaned_data['lab_name']
            history.note = form.cleaned_data['note']
            history.fin_time = datetime.now()
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
                his_def.lab_name = lab[0].name
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
    log.fin_time = datetime.now()
    log.confirm = 1
    log.save()
    return HttpResponseRedirect(reverse('courses:logView', args=(log.group_id,)))

def logView(request, group_id):
    group = get_object_or_404(CourseGroup, pk=group_id)
    if request.user.username != 'Teacher':
        raise Http404("只有教师具有此权限")
    students = list(StudentGroup.objects.filter(group=group))
    time_begin = datetime.combine(datetime.now(), time(0,0,0))
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
        else:
            students[i].complete = 0
    return render(request, 'courses/log_view.html', {'object_list':students})

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

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['course_id'])
        if self.request.session['schoolid'] != course.tea_id:
            return HttpResponseRedirect(reverse('courses:schedules', args=(course.id,)))
        form.instance.course_id = self.kwargs['course_id']
        return super().form_valid(form)

def delSchedule(request, sche_id):
    sche = get_object_or_404(CourseSchedule, pk=sche_id)
    course = sche.course
    if request.session['schoolid'] == course.tea_id:
        sche.delete()
    return HttpResponseRedirect(reverse('courses:schedules', args=(course.id,)))
