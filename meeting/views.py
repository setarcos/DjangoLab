from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import MeetingRoom, RoomAgenda
from .forms import AgendaForm
from django.urls import reverse
import datetime

def index(request):
    rooms = MeetingRoom.objects.all()
    if (rooms.count() == 0):
        raise Http404("没有定义会议室")
    if (rooms.count() > 1):
        return render(request, 'meeting/room_index.html', {'rooms': rooms})
    return HttpResponseRedirect(reverse('meeting:agenda_list', args=(rooms.first().id,)))

def agenda_add(request, room_id):
    room = get_object_or_404(MeetingRoom, pk=room_id)
    errors = []
    if (not request.session.has_key('schoolid')) or request.user.username != request.session['schoolid']:
        errors = ["你没有增加日程的权限"]
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = RoomAgenda(room=room)
            agenda.title = form.cleaned_data['note']
            agenda.start_time = form.cleaned_data['start']
            agenda.end_time = form.cleaned_data['end']
            agenda.userid = request.session['schoolid']
            agenda.week = form.cleaned_data['week']
            agenda.date = form.cleaned_data['date']
            agenda.username = request.session['realname']
            if form.cleaned_data['repeatable'] == '2':
                agenda.repeat = 1
            else:
                agenda.repeat = 0
                agenda.week = agenda.date.weekday() # make sure the week is right
            if agenda.collide():
                errors= errors + ["与其它日程存在冲突，请检查"]
            if agenda.repeat == 1:
                if (agenda.date - datetime.date.today()).days < 7:
                    errors = errors + ["每周重复日程请设定合适的截止日期"]
            if len(errors) == 0:
                agenda.save()
                return HttpResponseRedirect(reverse('meeting:agenda_list', args=(room.id,)))
    else:
        form = AgendaForm()
    return render(request, 'meeting/agenda_add.html', {'form': form, 'errors':errors})

def agenda_list(request, room_id):
    room = get_object_or_404(MeetingRoom, pk=room_id)
    td = datetime.date.today()
    td = td - datetime.timedelta(days=td.weekday()) # whole week
    agendas = RoomAgenda.objects.filter(room=room,date__gte=td)
    for a in agendas:
        a.view = ""
        if (a.repeat == 0) and (a.date > td + datetime.timedelta(days=6)):
            continue
        a.view = a.view + "left: %dpx;" % (a.week * 80 + 50)
        k = (a.start_time.hour - 5) * 40 + (a.start_time.minute / 6 * 4) - 5
        a.view = a.view + "top: %dpx;" % k
        k = (a.end_time.hour - a.start_time.hour) * 40 + (a.end_time.minute - a.start_time.minute) / 6 * 4
        a.view = a.view + "height: %dpx;" % k
    return render(request, 'meeting/agenda_list.html', {'agendas': agendas, 'room_id': room_id})

def agenda_view(request, agenda_id):
    agenda = get_object_or_404(RoomAgenda, pk=agenda_id)
    return render(request, 'meeting/agenda_view.html', {'agenda': agenda})

def agenda_del(request, agenda_id):
    agenda = get_object_or_404(RoomAgenda, pk=agenda_id)
    room = agenda.room
    if (agenda.userid == request.session['schoolid']) or (request.user.is_superuser):
        agenda.delete()
    return HttpResponseRedirect(reverse('meeting:agenda_list', args=(room.id,)))
