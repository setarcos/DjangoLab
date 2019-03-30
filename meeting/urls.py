from django.conf.urls import url
from . import views

app_name = 'meeting'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^agenda/list/(?P<room_id>[0-9]+)/$', views.agenda_list, name='agenda_list'),
    url(r'^agenda/add/(?P<room_id>[0-9]+)/$', views.agenda_add, name='agenda_add'),
    url(r'^agenda/view/(?P<agenda_id>[0-9]+)/$', views.agenda_view, name='agenda_view'),
    url(r'^agenda/del/(?P<agenda_id>[0-9]+)/$', views.agenda_del, name='agenda_del'),
]
