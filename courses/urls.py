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
    path('log/add/<int:group_id>/', views.logAdd, name='logAdd'),
]
