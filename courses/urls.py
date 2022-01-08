from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>/', views.detail, name='detail'),
    path('<int:course_id>/groups', views.groups, name='groups'),
    path('join/<int:group_id>/', views.joinGroup, name='joinGroup'),
    path('leave/<int:group_id>/', views.leaveGroup, name='leaveGroup'),
    path('group/<int:group_id>/', views.groupDetail, name='gdetail'),
    path('group/del/<int:group_id>/', views.delGroup, name='delGroup'),
    path('group/add/<int:course_id>/', views.AddGroupView.as_view(), name='addGroup'),
    path('log/add/<int:group_id>/', views.logAdd, name='logAdd'),
    path('<int:course_id>/schedule', views.ScheduleListView.as_view(), name='schedules'),
    path('schedule/add/<int:course_id>/', views.AddScheduleView.as_view(), name='addSchedule'),
    path('schedule/del/<int:sche_id>/', views.delSchedule, name='delSchedule'),
]
