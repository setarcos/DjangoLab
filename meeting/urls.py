from django.urls import re_path
from . import views

app_name = 'meeting'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^agenda/list/(?P<room_id>[0-9]+)/$', views.agenda_list, name='agenda_list'),
    re_path(r'^agenda/add/(?P<room_id>[0-9]+)/$', views.agenda_add, name='agenda_add'),
    re_path(r'^agenda/view/(?P<agenda_id>[0-9]+)/$', views.agenda_view, name='agenda_view'),
    re_path(r'^agenda/del/(?P<agenda_id>[0-9]+)/$', views.agenda_del, name='agenda_del'),
    re_path(r'^agenda/confirm/(?P<agenda_id>[0-9]+)/$', views.agenda_confirm, name='agenda_confirm'),
]
