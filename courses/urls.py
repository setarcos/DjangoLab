from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
]
