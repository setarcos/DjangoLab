from django.urls import path
from . import views

app_name = 'groceries'
urlpatterns = [
    path('', views.index, name='index'),
    path('lend/<int:lend_id>/', views.lendItem, name='lend'),
    path('hist/<int:lend_id>/', views.itemHist, name='hist'),
    path('edit/<int:lend_id>/', views.editItem, name='edit'),
    path('del/<int:lend_id>/', views.delItem, name='del'),
    path('new/', views.newItem, name='new'),
]
