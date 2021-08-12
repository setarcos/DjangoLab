from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
