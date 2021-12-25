from django.urls import path
from . import views

app_name = 'meeting'
urlpatterns = [
    path('', views.index, name='index'),
    path('agenda/list/<int:room_id>/', views.agenda_list, name='agenda_list'),
    path('agenda/add/<int:room_id>/', views.agenda_add, name='agenda_add'),
    path('agenda/view/<int:agenda_id>/', views.agenda_view, name='agenda_view'),
    path('agenda/del/<int:agenda_id>/', views.agenda_del, name='agenda_del'),
    path('agenda/confirm/<int:agenda_id>/', views.agenda_confirm, name='agenda_confirm'),
]
