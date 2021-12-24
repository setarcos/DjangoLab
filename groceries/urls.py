from django.urls import re_path
from . import views

app_name = 'groceries'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'lend/(?P<lend_id>[0-9]+)/$', views.lendItem, name='lend'),
    re_path(r'hist/(?P<lend_id>[0-9]+)/$', views.itemHist, name='hist'),
    re_path(r'edit/(?P<lend_id>[0-9]+)/$', views.editItem, name='edit'),
    re_path(r'del/(?P<lend_id>[0-9]+)/$', views.delItem, name='del'),
    re_path(r'new/$', views.newItem, name='new'),
]
