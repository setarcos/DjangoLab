from django.urls import path
from . import views

app_name = 'linux'
urlpatterns = [
    path('', views.index, name='index'),
]
