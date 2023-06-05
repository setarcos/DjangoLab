from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>/', views.detail, name='detail'),
    path('<int:course_id>/groups', views.groups, name='groups'),
    path('<int:course_id>/ghistory', views.ghistory, name='ghistory'),
    path('<int:course_id>/schedule', views.ScheduleListView.as_view(), name='schedules'),
    path('<int:course_id>/upload', views.courseUploadFile, name='upload'),
    path('<int:course_id>/files', views.courseFiles, name='files'),
    path('files/del/<int:file_id>', views.delFile, name='delFile'),
    path('join/<int:group_id>/', views.joinGroup, name='joinGroup'),
    path('leave/<int:group_id>/', views.leaveGroup, name='leaveGroup'),
    path('group/<int:group_id>/', views.groupDetail, name='gdetail'),
    path('group/del/<int:group_id>/', views.delGroup, name='delGroup'),
    path('group/add/<int:course_id>/', views.AddGroupView.as_view(), name='addGroup'),
    path('group/update/<int:group_id>/<str:stu_id>/', views.updateSeat, name='updateSeat'),
    path('log/add/<int:group_id>/', views.logAdd, name='logAdd'),
    path('log/<int:group_id>/', views.logView, name='logView'),
    path('log/confirm/<int:log_id>/', views.logConfirm, name='logConfirm'),
    path('schedule/add/<int:course_id>/', views.AddScheduleView.as_view(), name='addSchedule'),
    path('schedule/del/<int:sche_id>/', views.delSchedule, name='delSchedule'),
    path('schedule/update/<int:pk>/', views.UpdateScheduleView.as_view(), name='updateSchedule'),
    path('eva/<int:group_id>/<str:stu_id>/', views.evaView, name='evaView'),
    path('eva/add/<int:group_id>/<str:stu_id>/', views.AddStudentEvaView.as_view(), name='addEva'),
    path('eva/day/<int:group_id>/', views.evaDayView, name='evaDay'),
    path('eva/del/<int:pk>/', views.delEva, name='delEva'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:room_id>/', views.roomDetail, name='roomDetail'),
    path('update/<int:pk>/', views.CourseUpdateView.as_view(), name='courseUpdate'),
]
