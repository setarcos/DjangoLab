from django.urls import re_path
from . import views

app_name = 'home'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^auth/', views.auth, name='auth'),
    re_path(r'^logout/', views.logout_view, name='logout'),
]
