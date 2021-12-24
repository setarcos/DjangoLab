from django.urls import re_path
from . import views

app_name = 'courses'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^join/(?P<group_id>[0-9]+)/$', views.joinGroup, name='joinGroup'),
    re_path(r'^leave/(?P<group_id>[0-9]+)/$', views.leaveGroup, name='leaveGroup'),
    re_path(r'^group/(?P<group_id>[0-9]+)/$', views.groupDetail, name='gdetail'),
]
