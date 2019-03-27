from django.conf.urls import url
from . import views

app_name = 'groceries'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'lend/(?P<lend_id>[0-9]+)/$', views.lendItem, name='lend'),
    url(r'hist/(?P<lend_id>[0-9]+)/$', views.itemHist, name='hist'),
    url(r'edit/(?P<lend_id>[0-9]+)/$', views.editItem, name='edit'),
    url(r'del/(?P<lend_id>[0-9]+)/$', views.delItem, name='del'),
    url(r'new/$', views.newItem, name='new'),
]
